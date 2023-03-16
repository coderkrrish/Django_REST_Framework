# #In terms of django rest framework serialization means converting complex data into python dictionary and de-serialization means converting python dictionary to complex data. Serializer will handle both the things that is serialization and deserialization


# #JsonRender = Python to Json
# #JsonParser = Json to Python

from rest_framework import serializers
from .models import Student, Employee

# class StudentSerializer(serializers.Serializer):
#     # id = serializers.IntegerField()
#     name = serializers.CharField(max_length = 100)
#     age = serializers.IntegerField()
#     address = serializers.CharField(max_length = 100)
#     marks = serializers.IntegerField()
#     is_active = serializers.BooleanField()


#     def create(self,validated_data):
#         print('In Create Method',validated_data)
#         return Student.objects.create(**validated_data)
    

#     def update(self, instance, validated_data):
#     #    print("In Update Method",instance,validated_data)
#         instance.name = validated_data.get("name",instance.name)
#         instance.age  = validated_data.get("age",instance.age)
#         instance.marks = validated_data.get("marks",instance.marks)
#         instance.address= validated_data.get("address",instance.address)
#         instance.is_active = validated_data.get("is_active",instance.is_active)
#         instance.save()
#         return instance


#     # def validate_name(self, value):
#     #     print("In Validate")
#     #     if 'i' not in value.lower():
#     #         raise serializers.ValidationError("Name dosent have i in name")
#     #     return value

#     # def validate_age(self,value):
#     #     print("In Validate")
#     #     if value < 18:
#     #         raise serializers.ValidationError("Age Should Be Greater Than 18")
#     #     return value


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = "__all__"

        #If we want to set constaraints like read only ,write only on fields then it is done by using following way
        # read_only_fields = ["name"]  #Here name is set to read only SO  if we create data name will not be added and if we update data name will remain as it is it won change

        # extra_kwargs = {"name":{"read_only" :True}, "age" :{"write_only" : True}}  #IF we want to set above constraints on multiple fileds 

        # extra_kwargs = {"address" :{"read_only" :True , "write_only" :True}}  #May not set both `read_only` and `write_only`  we can no set both constraints on a fields 

        # exclude = ("id","name", "address", "is_active")  #Excluding a field if we dont want that field


    # def create(self,validated_data):  # Here we are overriding the create method
    #     print("In Create Method")
    #     stud  = Student.objects.create(**validated_data)
    #     return stud


class EmployeeSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields  = "__all__"


