from django.contrib import admin
from .models import Question


##admin에 질문모델 등록하기
#admin.site.register(Question)



##Question 모델에 세부 기능을 추가할 수 있는 QuestionAdmin 클래스를 생성하고
##제목 검색을 위해 search_fields 속성에 'subject'를 추가해 주었다.

class QuestionAdmin(admin.ModelAdmin):
    search_fields = ['subject']


admin.site.register(Question, QuestionAdmin)
