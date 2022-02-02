from django.db import models
from django.contrib.auth.models import User

class Question(models.Model):
    subject = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name= 'author_question')
    modify_date = models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(User, related_name='voter_question')  # 추천인 추가
    create_date = models.DateTimeField()
    def __str__(self):
        return self.subject


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_answer')
    modify_date = models.DateTimeField(null=True, blank=True)
    # null=True는 데이터베이스에서 modify_date 칼럼에 null을 허용한다는 의미이며,
    # blank=True는 form.is_valid()를 통한 입력 데이터 검사 시 값이 없어도 된다는 의미이다.
    # 즉, null=True, blank=True는 어떤 조건으로든 값을 비워둘 수 있음을 의미한다

    create_date = models.DateTimeField()
    voter = models.ManyToManyField(User, related_name='voter_answer')

class Comment(models.Model):
    answer = models.ForeignKey(Answer, null=True, blank=True, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_comment')
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(User, related_name='voter_comment')

