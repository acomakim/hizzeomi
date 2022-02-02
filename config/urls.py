from django.contrib import admin
from django.urls import path, include
from pybo.views import base_views


# from pybo import views 더 이상 필요하지 않으므로 삭제

urlpatterns = [
    path('admin/', admin.site.urls),
    path('pybo/', include('pybo.urls')), # pybo앱 하단의 urls.py로 연결
    path('common/', include('common.urls')),
    path('', base_views.index, name='index'),  # '/' 에 해당되는 path
]




