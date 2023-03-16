from rest_framework_swagger.views import get_swagger_view
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.generics import (ListCreateAPIView, RetrieveDestroyAPIView,
                                     RetrieveUpdateAPIView,
                                     RetrieveUpdateDestroyAPIView)
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin, RetrieveModelMixin,
                                   UpdateModelMixin)
from rest_framework.generics import GenericAPIView
from django.views import View
from django.utils.decorators import method_decorator
import io
import json

from django.contrib.auth import authenticate
from django.db import transaction
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.urls import re_path as url
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.authentication import (BasicAuthentication,
                                           RemoteUserAuthentication,
                                           SessionAuthentication,
                                           TokenAuthentication)
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from .models import Employee, Student
from .serializers import EmployeeSerilizer, StudentSerializer

# Create your views here.


def get_student(request, id):
    stud_by_id = Student.objects.get(id=id)  # it will give the complex data
    # print(stud_by_id.__dict__) #{'_state': <django.db.models.base.ModelState object at 0x00000230265010C0>, 'id': 1, 'name': 'Manasvi', 'age': 19, 'address': 'Solapur', 'marks': 99}

    # Other then using the json dumps method we can use the serializer for converting complex data into python dict
    python_data = StudentSerializer(stud_by_id)
    bytes_data = JSONRenderer().render(python_data.data)
    # <class 'bytes'> The json renderer will give the data into bytes form
    print(type(bytes_data))

    # Here content_type will give the bytes_data into json string
    return HttpResponse(bytes_data, content_type="application/json")

    # stud_by_id.__dict__.pop("_state") #Here the state will be removed from the dict
    # # print(stud_by_id.__dict__)#{'id': 1, 'name': 'Manasvi', 'age': 19, 'address': 'Solapur', 'marks': 99}  This is stateless dictionary

    # data  = json.dumps(stud_by_id.__dict__) #above dict is python dict to convert the python dict into json data dumps is used and passed the data to httpresponse
    # return HttpResponse("Success")  #Here the data is Json data it will get loaded to the page

# Get All Stuents


def get_all_students(request):
    all_studs = Student.objects.all()
    # Here the data is multiple data thats why many is passed
    python_data = StudentSerializer(all_studs, many=True)
    bytes_data = JSONRenderer().render(python_data.data)
    return HttpResponse(bytes_data, content_type="application/json", status=status.HTTP_200_OK)


# Creating Student


@csrf_exempt
@api_view(["POST"])
def create_student(request):
    if request.method == "POST":
        # b'{\r\n    "name": "Jay",\r\n    "age": 23,\r\n    "address": "Mumbai",\r\n    "marks": 78\r\n}'
        bytes_data = request.body
        # Here we have converted above bytes data into json str
        my_json = bytes_data.decode("utf8").replace("'", '"')
        # print(my_json)
        # print(type(my_json))   #<class 'str'>

        # Here by using json.loads we are converting the json str into python dict
        json_to_py_dict = json.loads(my_json)
        # print(json_to_py_dict) #{'name': 'Jay', 'age': 23, 'address': 'Mumbai', 'marks': 78}
        # print(type(json_to_py_dict)) #<class 'dict'>

        # for adding the above python dict data into database it need to be converted into complex data(complex data means into a queryset)

        ser = StudentSerializer(data=json_to_py_dict)
        if ser.is_valid():
            data = ser.save()
            print(data.__dict__)
            data.__dict__.pop("_state")

            # success_msg  ={"Msg":"Data Inserted Successfully"}
            json_success_msg = json.dumps(data.__dict__)
            return HttpResponse(json_success_msg, content_type="application/json", status=status.HTTP_201_CREATED)
            # print(request.build_absolute_uri()) #http://127.0.0.1:8000/api/create-student/

        else:
            error_msg = {"Msg": "Invalid JSON Data"}
            json_error_msg = json.dumps(error_msg)
            return HttpResponse(json_error_msg, content_type="application/json", status=status.HTTP_404_NOT_FOUND)

    else:
        error_msg = {"Msg": "Only Post Method is Allowded"}
        json_error_msg = json.dumps(error_msg)
        return HttpResponse(json_error_msg, content_type="application/json", status=status.HTTP_405_METHOD_NOT_ALLOWED)


def common_lines(request):
    bytes_data = request.body
    my_json = bytes_data.decode("utf8").replace("'", '"')
    json_to_py_dict = json.loads(my_json)
    return json_to_py_dict


@csrf_exempt
@api_view(["GET", "POST", "PUT", "PATCH", "DELETE"])
def all_stud_operations(request):
    if request.method == "GET":
        json_to_py_dict = common_lines(request)
        print(json_to_py_dict)
        sid = json_to_py_dict.get("id")
        if sid:
            stud_obj = Student.objects.get(id=sid)
            python_data = StudentSerializer(stud_obj)
            bytes_data = JSONRenderer().render(python_data.data)
            # return HttpResponse(bytes_data,content_type = "application/json")
            # This is shortcut for httpresponse
            return JsonResponse(python_data.data, safe=False)

        all_students = Student.objects.all()
        python_dict = StudentSerializer(all_students, many=True)
        bytes_data = JSONRenderer().render(python_dict.data)
        # return HttpResponse(bytes_data,content_type = "application/json")
        return JsonResponse(python_dict.data, safe=False)
        # return JsonResponse({"Msg":"Success"})

    elif request.method == "POST":
        # bytes_data= request.body  #b'{\r\n    "name": "Jay",\r\n    "age": 23,\r\n    "address": "Mumbai",\r\n    "marks": 78\r\n}'
        # my_json= bytes_data.decode("utf8").replace("'", '"') #Here we have converted above bytes data into json str
        # print(my_json)
        # print(type(my_json))   #<class 'str'>

        # json_to_py_dict = json.loads(my_json)  #Here by using json.loads we are converting the json str into python dict
        # print(json_to_py_dict) #{'name': 'Jay', 'age': 23, 'address': 'Mumbai', 'marks': 78}
        # print(type(json_to_py_dict)) #<class 'dict'>

        json_to_py_dict = common_lines(request)
        # for adding the above python dict data into database it need to be converted into complex data(complex data means into a queryset)
        ser = StudentSerializer(data=json_to_py_dict)
        if ser.is_valid():
            data = ser.save()
            print(data.__dict__)
            data.__dict__.pop("_state")

            # success_msg  ={"Msg":"Data Inserted Successfully"}
            json_success_msg = json.dumps(data.__dict__)
            return HttpResponse(json_success_msg, content_type="application/json", status=status.HTTP_201_CREATED)
            # print(request.build_absolute_uri()) #http://127.0.0.1:8000/api/create-student/

        else:
            error_msg = {"Msg": "Invalid JSON Data"}
            json_error_msg = json.dumps(error_msg)
            return HttpResponse(json_error_msg, content_type="application/json", status=status.HTTP_404_NOT_FOUND)

    elif request.method == "PUT":
        json_to_py_dict = common_lines(request)
        sid = json_to_py_dict.get("id")
        stud_obj = Student.objects.get(id=sid)
        ser = StudentSerializer(instance=stud_obj, data=json_to_py_dict)
        if ser.is_valid():
            data = ser.save()
            print(data.__dict__)
            data.__dict__.pop("_state")
            resp_dict = {"response_msg": "Data Updated Successfully"}
            resp_dict.update({"returned_data": data.__dict__})
            json_msg = json.dumps(resp_dict)
            return HttpResponse(json_msg, content_type="application/json", status=status.HTTP_200_OK)
        else:
            return JsonResponse({"error": ser.errors})
        # return JsonResponse({"msg":"SUCCESS"})

    elif request.method == "PATCH":
        json_to_py_dict = common_lines(request)
        print(json_to_py_dict)
        sid = json_to_py_dict.get("id")
        stud_obj = Student.objects.get(id=sid)
        ser = StudentSerializer(
            instance=stud_obj, data=json_to_py_dict, partial=True)
        if ser.is_valid():
            data = ser.save()
        #    print(data.__dict__)
            data.__dict__.pop("_state")
            print(data.__dict__)
            resp_dict = {"response_msg": "Data Updated Successfully"}
            resp_dict.update({"returned_data": data.__dict__})
            json_msg = json.dumps(resp_dict)
            return HttpResponse(json_msg, content_type="application/json", status=status.HTTP_200_OK)
        else:
            return JsonResponse({"error": ser.errors})

    # elif request.method =="DELETE":
        # stud_obj = Student.objects.get(id = 11).delete()
        # return HttpResponse("Deleted Successfully", status = status.HTTP_204_NO_CONTENT,content_type = "application/json")


# Class Based Views


@method_decorator(csrf_exempt, name="dispatch")
class StudentAPI(View):
    def get(self, request, *args, **kwargs):
        json_to_py_dict = common_lines(request)
        print(json_to_py_dict)
        sid = json_to_py_dict.get("id")
        if sid:
            try:
                stud_obj = Student.objects.get(id=sid)
            except Student.DoesNotExist:
                return JsonResponse({"msg": "Data Not Present For Given ID"})
            python_data = StudentSerializer(stud_obj)
            return JsonResponse(python_data.data)

        all_studs = Student.objects.all()
        python_data = StudentSerializer(all_studs, many=True)
        return JsonResponse(python_data.data, safe=False)

    def post(self, request, *args, **kwargs):
        json_to_py_dict = common_lines(request)
        ser = StudentSerializer(data=json_to_py_dict)
        if ser.is_valid():
            data = ser.save()
            data.__dict__.pop("_state")
            print(data.__dict__)
            json_success_msg = json.dumps(data.__dict__)
            return HttpResponse(json_success_msg, content_type="application/json", status=status.HTTP_201_CREATED)
        else:
            err_msg = {"msg": "Invalid Json data"}
            json_err_msg = json.dumps(err_msg)
            return HttpResponse(json_err_msg, content_type="application/json", status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        json_to_py_dict = common_lines(request)
        sid = json_to_py_dict.get("id")
        stud_obj = Student.objects.get(id=sid)
        ser = StudentSerializer(instance=stud_obj, data=json_to_py_dict)
        if ser.is_valid():
            data = ser.save()
            print(data.__dict__)
            data.__dict__.pop("_state")
            resp_dict = {"resp_message": "Data Updated Successfully"}
            resp_dict.update({"returned_data": data.__dict__})
            json_msg = json.dumps(resp_dict)
            return HttpResponse(json_msg, content_type="application/json", status=status.HTTP_200_OK)

        else:
            return JsonResponse({"err": ser.errors})

    def patch(self, request, *args, **kwargs):
        json_to_py_dict = common_lines(request)
        sid = json_to_py_dict.get("id")
        stud_obj = Student.objects.get(id=sid)
        ser = StudentSerializer(
            instance=stud_obj, data=json_to_py_dict, partial=True)
        if ser.is_valid():
            data = ser.save()
            print(data.__dict__)
            data.__dict__.pop("_state")
            resp_dict = {"rep_message": "Data Partially Updated Successfully"}
            resp_dict.update({"returned data": data.__dict__})
            json_msg = json.dumps(resp_dict)
            return HttpResponse(json_msg, content_type="application/json", status=status.HTTP_200_OK)
        else:
            return JsonResponse({"err": ser.errors})

    def delete(self, request, *args, **kwargs):
        json_to_py_dict = common_lines(request)
        sid = json_to_py_dict.get("id")
        stud_obj = Student.objects.get(id=sid)
        stud_obj.delete()
        return JsonResponse({"msg": "Data Deleted Successfully"}, content_type="application/json", status=status.HTTP_404_NOT_FOUND)


# Optimizing The Function Based Views Written Above


@api_view(["GET", "POST", "PUT", "PATCH", "DELETE"])
def optimized_stud(request, pk=None):
    if request.method == "GET":
        # print(type(request.data)) #<class 'dict'>
        # sid = request.data.get("id")
        sid = pk
        if sid:
            try:
                stud_obj = Student.objects.get(id=sid)
                ser = StudentSerializer(stud_obj)
                return Response(ser.data)
            except Student.DoesNotExist:
                return JsonResponse({"Msg": "Data Does Not Exist For Given ID"})
        else:

            all_studs = Student.objects.all()
            ser = StudentSerializer(all_studs, many=True)
            return Response(ser.data)
            # return HttpResponse("In Optimized Function Based Views")

    elif request.method == "POST":
        py_dict = request.data
        ser = StudentSerializer(data=py_dict)
        if ser.is_valid():
            with transaction.atomic():
                returned_data = ser.save()
                returned_data.__dict__.pop("_state")
                # print(returned_data)
                return Response({"Msg": "Data Created Successfully", "Created_Data": returned_data.__dict__}, status=status.HTTP_201_CREATED)
        else:
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "PUT":
        py_dict = request.data
        # sid = py_dict.get("id")
        sid = pk
        stud_obj = Student.objects.get(id=sid)
        ser = StudentSerializer(instance=stud_obj, data=py_dict)
        if ser.is_valid():
            data = ser.save()
            data.__dict__.pop("_state")
            return Response({"msg": f"Data Updated For ID {sid} Successfully", "updated_data": data.__dict__}, status=status.HTTP_200_OK)

        else:
            return Response(ser.errors)

    elif request.method == "PATCH":
        py_dict = request.data
        # sid = py_dict.get("id")
        sid = pk
        stud_obj = Student.objects.get(id=sid)
        ser = StudentSerializer(instance=stud_obj, data=py_dict, partial=True)
        if ser.is_valid():
            data = ser.save()
            data.__dict__.pop("_state")
            return Response({"msg": f"Partial Data Updated For  ID {sid} successfully", "returned_data": data.__dict__}, status=status.HTTP_200_OK)

        else:
            return Response(ser.errors)

    elif request.method == "DELETE":
        py_dict = request.data
        # sid = py_dict.get("id")
        sid = pk
        stud = Student.objects.get(id=sid)
        stud.delete()
        return Response({"msg": f" Data Deleted Successfully for  ID {sid}"}, status=status.HTTP_404_NOT_FOUND)


# --------------------------------------------Generic API Views with Mixins

# The Hierarchy of Views is View -->API View-->GenericAPI View

# from where to import Generic Views

# This Generic API View contains two things
# 1)queryset = Model.objects.all
# 2)serializer_class

# In this app case the Model = Student and the serializer_class = StudentSerializer


class StudentList(GenericAPIView, ListModelMixin):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def get(self, request, *args, **kwargs):
        return self.list(self, request, *args, **kwargs)


class StudentCreate(GenericAPIView, CreateModelMixin):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class StudentRetrieve(GenericAPIView, RetrieveModelMixin):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(self, request, *args, **kwargs)


class StudentUpdate(GenericAPIView, UpdateModelMixin):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class StudentPartialUpdate(GenericAPIView, UpdateModelMixin):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class StudentDelete(GenericAPIView, DestroyModelMixin):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"Msg": "Data Deleted Successfully"}, status=status.HTTP_204_NO_CONTENT)


# -------------------------Combined Mixins
# Here we will be combining those mixins which needs ID in one class and those mixins those dont need an ID in another class


class StudentListCreate(GenericAPIView, ListModelMixin, CreateModelMixin):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def get(self, request, *args, **kwargs):
        return self.list(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class StudentRetrieveUpdatePartialUpdateDestroy(GenericAPIView, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin):
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ---------------Concreate API Views

# In Concreate API Views we are combining the GenericAPIView and Individual Mixins and handler methods(get,post, put,patch ,delete)


class StudentCList(ListAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class StudentCCreate(CreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class StudentCRetrieve(RetrieveAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class StudentCUpdate(UpdateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class StudentCDelete(DestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


# Combined Concreate API's


class StudentCCListCreate(ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class StudentCCRetrieveDestroy(RetrieveDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class StudentCCRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class StudentCCRetrieveUpdate(RetrieveUpdateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


# ViewSets : ViewSets are the methods which contains repeated code
# ViewSet have the following methods list(), create(), retrieve(), update(), partialupdate(), destroy()


class StudentViewset(ViewSet):
    def list(self, request):
        queryset = Student.objects.all()
        serializer = StudentSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        data = request.data
        serializer = StudentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk):
        stud_obj = Student.objects.get(id=pk)
        serializer = StudentSerializer(stud_obj)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        data = request.data
        stud_obj = Student.objects.get(id=pk)
        ser = StudentSerializer(instance=stud_obj, data=data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data, status=status.HTTP_200_OK)
        else:
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        data = request.data
        stud_obj = Student.objects.get(id=pk)
        ser = StudentSerializer(instance=stud_obj, data=data, partial=True)
        if ser.is_valid():
            ser.save()
            return Response(ser.data, status=status.HTTP_200_OK)
        else:
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        data = request.data
        stud_obj = Student.objects.get(id=pk)
        stud_obj.delete()
        return Response({"msg": "Data Deleted Successfully"}, status=status.HTTP_204_NO_CONTENT)


class StudentModelViewSet(ModelViewSet):
    # queryset = Student.objects.all()  #1st Way to get all active and inactive students
    # Here it will give only the active data
    queryset = Student.objects.filter(is_active=True)
    serializer_class = StudentSerializer
    # lookup_field = "name"   #if you want to search any recored other than "id" then pass the field name in lookup field
    
    # authentication_classes = [BasicAuthentication]
    # permission_classes = [IsAuthenticated]

    # def list(self, request, *args, **kwargs):   #2nd Way to get all active and inactive students.Here list method of ListModelMixin is overridden.But It will only limited to "GET" method So this is not a preferable way. 1st way is always preferable beause it is not limited to only "GET" method
    #     queryset = Student.objects.filter(is_active = False)

    #     page = self.paginate_queryset(queryset)
    #     if page is not None:
    #         serializer = self.get_serializer(page, many=True)
    #         return self.get_paginated_response(serializer.data)

    #     serializer = self.get_serializer(queryset, many=True)
    #     return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response(data={"Msg": "Data Soft Deleted Successfully"}, status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'], url_name='inactive-studs',
            url_path='inactive-studs')
    # 2nd Way to get all active and inactive students.Here list method of ListModelMixin is overridden.But It will only limited to "GET" method So this is not a preferable way. 1st way is always preferable beause it is not limited to only "GET" method
    def get_inactive_data(self, request, *args, **kwargs):
        queryset = Student.objects.filter(is_active=False)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], url_name='media-delete',
            url_path='restore-stud/(?P<pk>[^/.]+)')
    def restore_data(self, request, pk = None):

        stud_obj = Student.objects.get(id =pk)
        stud_obj.is_active = True
        stud_obj.save()
        return Response({"Msg" : "Data Restored Successfully"}, status  =status.HTTP_200_OK)
        

    # authentication_classes = [SessionAuthentication]
    # permission_classes = [IsAuthenticated]

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    


class EmployeeModelViewsSet(ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerilizer
    # authentication_classes = [BasicAuthentication]
    # permission_classes = [IsAuthenticated]


schema_view = get_swagger_view(title='Student API')

urlpatterns = [
    url(r'^$', schema_view)
]


@csrf_exempt
@api_view(['POST'])
@permission_classes((AllowAny,))
def generate_token(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({"error" : "Please Provide Both Username And Password"}, status= status.HTTP_400_BAD_REQUEST)
    user = authenticate(username = username, password = password)
    if not user:
        return Response({"error": "Invalid Credentials"} , status = status.HTTP_404_NOT_FOUND)

    token , flag = Token.objects.get_or_create(user = user)
    print(token,flag)
    return Response({"token" : token.key}, status = status.HTTP_200_OK)
