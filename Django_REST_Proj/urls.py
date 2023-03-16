"""Django_REST_Proj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from REST_App import views
from REST_App.urls import new_urlpatterns
from django.urls import re_path as url


from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.documentation import include_docs_urls
from rest_framework import permissions

from rest_framework.authtoken.views import obtain_auth_token

from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/get-student/<int:id>", views.get_student),
    path("api/get-all-students/",views.get_all_students),
    path("api/create-student/", views.create_student),



    #CRUD Operations in one function
    path("api/all-operations/",views.all_stud_operations),


    #Class Based Views URL's
    path("api/stud-class-api/", views.StudentAPI.as_view()), 


    #Optimized Function Based Views URL's
    path("api/optimized-stud-func/", views.optimized_stud),
    path("api/optimized-stud-func/<int:pk>/", views.optimized_stud),


    #Generic API Views with Mixins URL's
    path("api/generic-list-stud/", views.StudentList.as_view()),
    path("api/generic-create-stud/", views.StudentCreate.as_view()),
    path("api/generic-retrieve-stud/<int:pk>/", views.StudentRetrieve.as_view()),
    path("api/generic-update-stud/<int:pk>/", views.StudentUpdate.as_view()),
    path("api/generic-partial-update-stud/<int:pk>/", views.StudentPartialUpdate.as_view()),
    path("api/generic-delete-stud/<int:pk>/", views.StudentDelete.as_view()),


    #Combined Mixins URL's
    path("api/stud-list-create/", views.StudentListCreate.as_view()),
    path("api/stud-retrieve-update-delete/<int:pk>", views.StudentRetrieveUpdatePartialUpdateDestroy.as_view()),



    #Concreate API Views
    path("api/stud-c-list/", views.StudentCList.as_view()),
    path("api/stud-c-create/", views.StudentCCreate.as_view()),
    path("api/stud-c-retrieve/<int:pk>/", views.StudentCRetrieve.as_view()),
    path("api/stud-c-update/<int:pk>/", views.StudentCUpdate.as_view()),
    path("api/stud-c-delete/<int:pk>/", views.StudentCDelete.as_view()),

  

    #Combined Concreate API
    path("api/stud-cc-list-create/", views.StudentCCListCreate.as_view()),
    path("api/stud-cc-retr-dest/<int:pk>/", views.StudentCCRetrieveDestroy.as_view()),
    path("api/stud-cc-retr-update-destroy/<int:pk>/", views.StudentCCRetrieveUpdateDestroy.as_view()),
    path("api/stud-cc-retr-update/", views.StudentCCRetrieveUpdate.as_view()),
    


    # #ViewsSet URL's

    # path("api/viewset-stud/", views.StudentViewset.as_view({'get':'list'})),
    # path("api/viewset-stud/<int:pk>/", views.StudentViewset.as_view({'get':'retrieve'})),
    # path("api/viewset-stud/", views.StudentViewset.as_view({'post':'create'})),
    # path("api/viewset-stud/<int:pk>", views.StudentViewset.as_view({'delete':'destroy'})),
    # path("api/viewset-stud/<int:pk>", views.StudentViewset.as_view({'put':'update'})),
    # 
 

    path("api/", include(new_urlpatterns)),



    path("api/", include(new_urlpatterns)),
    url(r'^api-auth/', include('rest_framework.urls', namespace = 'rest_framework')), 
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'), #Here the user will obtain an token for himself This is the Built in function 
    path('api/generate-token/', views.generate_token),  #Here we have created a function to generate token



    #JWT URL's
    path('api/token/', jwt_views.TokenObtainPairView.as_view()),
    path('api/refresh-token/', jwt_views.TokenRefreshView.as_view()),




]


schema_view = get_schema_view(
    openapi.Info(
        title="Students API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
   
)

urlpatterns += [
    path('docs/', include_docs_urls(title='Student Api')),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
]


