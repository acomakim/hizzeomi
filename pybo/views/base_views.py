from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404

from ..models import Question
from django.db.models import Q, Count

#질문목록 매핑
def index(request):
    """
    pybo 목록 출력
    """
    question_list = Question.objects.order_by('-create_date')
    context = {'question_list': question_list}
    #render는 파이썬 데이터를 템플릿에 적용하여 HTML로 반환하는 함수이다

    # 입력 파라미터
    page = request.GET.get('page', '1')  # 페이지
    kw = request.GET.get('kw', '')  # 검색어
    so = request.GET.get('so', 'recent')  # 정렬기준

    # 정렬
    if so == 'recommend':
        question_list = Question.objects.annotate(num_voter=Count('voter')).order_by('-num_voter', '-create_date')
    elif so == 'popular':
        question_list = Question.objects.annotate(num_answer=Count('answer')).order_by('-num_answer', '-create_date')
    else:  # recent
        question_list = Question.objects.order_by('-create_date')

    # Question.objects.annotate(num_voter=Count('voter'))는 Question의 기존 속성인
    # author, subject, content, create_date, modify_date, voter에 num_voter라는
    # 속성을 하나 더 추가한다고 생각하면 쉽다. 이렇게 annotate로 num_voter를 지정하면
    # filter나 order_by에서 num_voter를 사용할 수 있게 된다. 여기서 질문의 추천수인
    # num_voter는 Count('voter') 처럼 Count 함수를 사용하여 얻을 수 있다.
    # Count('voter') 는 이 질문의 추천수를 의미한다.
    # order_by('-num_voter', '-create_date') 처럼 order_by 함수에 1개 이상의 파라미터
    # 가 전달될 때에는 앞의 항목부터 우선순위를 갖게 되어 추천수로 먼저 정렬하고 추천수가
    # 같을경우에는 최신순으로 정렬하게 된다.


    # 검색
    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw) |  # 제목검색
            Q(content__icontains=kw) |  # 내용검색
            Q(author__username__icontains=kw) |  # 질문 글쓴이검색
            Q(answer__author__username__icontains=kw)  # 답변 글쓴이검색
        ).distinct()  # 중복건 제외 처리


    # 페이징처리
    paginator = Paginator(question_list, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)

    context = {'question_list': page_obj, 'page': page, 'kw': kw, 'so':so}
    return render(request, 'pybo/question_list.html', context)



# index 함수와 크게 다른 부분은 없다. 다만 detail 함수 호출시 전달되는 매개변수가
# request 외에 question_id가 추가되었다. 매개변수 question_id에는 URL 매핑시 저장된
# question_id가 전달된다.
#
# 즉, http://localhost:8000/pybo/2/ 페이지가 요청되면 최종적으로 detail 함수의
# 매개변수 question_id에는 2라는 값이 전달된다.



def detail(request, question_id):
    """
    pybo 내용 출력
    """
    question = get_object_or_404(Question, pk=question_id)  # 없는 데이터 404에러 반환
    context = {'question': question}
    return render(request, 'pybo/question_detail.html', context)

# HTTP 주요 응답코드의 종류
#
# 오류코드	설명
# 200	성공 (OK)
# 500	서버오류 (Internal Server Error )
# 404	서버가 요청한 페이지(Resource)를 찾을 수 없음 (Not Found)