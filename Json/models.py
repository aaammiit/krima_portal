from django.db import models
from django.contrib.auth.models import User
from django import forms


# Create your models here.

class Admin(models.Model):
    username=models.CharField(max_length=100)
    password=models.CharField(max_length=100)

class My_Upload_file(models.Model):
    file=models.FileField()
    seg=models.CharField(max_length=100)
    count=models.IntegerField(null=True)
    from_date=models.CharField(max_length=100,null=True)
    to_date=models.CharField(max_length=100,null=True)
    status=models.BooleanField(default=False)
    def __str__(self):
        return self.file.name
    


class PM(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    def __str__(self):
        u=self.user.first_name+'-'+self.user.last_name
        return u
    

    
class Push_to_pm_file(models.Model):
    my_file=models.ForeignKey(My_Upload_file,on_delete=models.CASCADE)
    status=models.BooleanField(default=False)
    
class Add_col(models.Model):
    eid=models.IntegerField()
    file=models.ForeignKey(Push_to_pm_file,on_delete=models.CASCADE)
    st=models.BooleanField(default=False)


   

class Qc_user(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    
    def __str__(self):
        u=self.user.first_name+'-'+self.user.last_name
        return u


class my_Qc_data(models.Model):
    my_file=models.ForeignKey(Push_to_pm_file,on_delete=models.CASCADE)
    qc_file=models.FileField(upload_to='qc')
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    start=models.IntegerField(default=0)
    end=models.IntegerField()
    msg=models.CharField(max_length=100,default='')
    status=models.BooleanField(default=False)

class Add_col_qc(models.Model):
    # eid=models.IntegerField()
    file=models.ForeignKey(my_Qc_data,on_delete=models.CASCADE)
    st=models.BooleanField(default=False)
    col=models.CharField(max_length=100,default='')
    data=models.CharField(max_length=100,default='')


class qc_Form(forms.ModelForm):
    class Meta:
        model=my_Qc_data
        fields=['user','msg']



class ED_User(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    
    def __str__(self):
        u=self.user.first_name+'-'+self.user.last_name
        return u

class Editor_push(models.Model):
    Ed=models.ForeignKey(ED_User,on_delete=models.CASCADE)
    qc_data=models.ForeignKey(my_Qc_data,on_delete=models.CASCADE)
    qc_user=models.ForeignKey(Qc_user,on_delete=models.CASCADE)
   
    sta=models.BooleanField(default=False)


    def __str__(self):
        return self.qc_data.qc_file.name
    

class pushForm(forms.ModelForm):
    class Meta:
        model=Editor_push
        fields=['Ed']

class Final_data_PM(models.Model):
    editior=models.ForeignKey(ED_User,on_delete=models.CASCADE)
    Edited_file=models.ForeignKey(Editor_push,on_delete=models.CASCADE)
    pm=models.ForeignKey(PM,on_delete=models.CASCADE)    
    date=models.DateField(auto_now=True)    
    status=models.BooleanField(default=False)


class Final_form(forms.ModelForm):
    class Meta:
        model=Final_data_PM
        fields=['pm','status']

        
class File_name(models.Model):
    name=models.CharField(max_length=100)
