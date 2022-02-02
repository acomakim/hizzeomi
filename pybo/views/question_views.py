from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from ..forms import QuestionForm
from ..models import Question

@login_required(login_url='common:login')
def question_create(request):
    """
    pybo 질문등록
    """
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)      # 임시저장함, QuestionForm 에 create_date 속성이 정의되지 않음
            question.create_date = timezone.now()   # 객체 question에 저장 후 create_date 속성 생성
            question.author = request.user
            question.save()
            return redirect('pybo:index')
    else:
        form = QuestionForm()
    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)



# 가장 눈에 띄는 부분은 동일한 URL 요청을 POST, GET 요청 방식에 따라 다르게 처리한 부분이다.
# 질문 목록 화면에서 "질문 등록하기" 버튼을 클릭한 경우에는 /pybo/question/create/ 페이지가
# GET 방식으로 요청되어 question_create 함수가 실행된다. 왜냐하면
# <a href="{% url 'pybo:question_create' %}" class="btn btn-primary">질문 등록하기</a>과 같이 링크를 통해 페이지를 요청할
# 경우에는 무조건 GET 방식이 사용되기 때문이다. 따라서 이 경우에는 request.method 값이 GET이 되어 if .. else .. 에서
# else 구문을 타게 되어 결국 질문 등록 화면을 보여 줄 것이다.
#
# 그리고 질문 등록 화면에서 subject, content 항목에 값을 기입하고 "저장하기" 버튼을 클릭하면 이번에는
# 동일한 /pybo/question/create/ 페이지가 POST방식으로 요청된다. 왜냐하면 앞서 설명했듯이 form 태그에 action 속성이 지정되지 않으면
# 현재 페이지가 디폴트 action으로 설정되기 때문이다.
#
# 따라서 질문 등록 화면에서 "저장하기" 버튼을 클릭하면 question_create 함수가 실행되고
# request.method 값은 POST가 되어 다음 코드들이 실행될 것이다.


@login_required(login_url='common:login')
def question_modify(request, question_id):
    """
    pybo 질문수정
    """
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('pybo:detail', question_id=question.id)

    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)
        # 위 코드의 의미는 instance를 기준으로 QuestionForm을 생성하지만
        # request.POST의 값으로 덮어쓰라는 의미이다. 따라서 질문 수정화면에서
        # 제목 또는 내용을 변경하여 POST 요청하면 변경된 내용이 QuestionForm에 저장될 것이다.

        if form.is_valid():
            question = form.save(commit=False)
            question.modify_date = timezone.now()  # 수정일시 저장
            question.save()
            return redirect('pybo:detail', question_id=question.id)
    else:
        form = QuestionForm(instance=question)
    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)


@login_required(login_url='common:login')
def question_delete(request, question_id):
    """
    pybo 질문삭제
    """
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('pybo:detail', question_id=question.id)
    question.delete()
    return redirect('pybo:index')