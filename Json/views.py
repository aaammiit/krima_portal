from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate,logout
from .models import *
from datetime import datetime
import json
from Main import settings
import pandas as pd

from django.contrib import messages  

# Create your views here.
def Home(request):
    if request.method=='POST':
        u=request.POST.get('un')
        p=request.POST.get('p')
        user=authenticate(User,username=u,password=p)  
        try: 
            if user.is_staff:
                request.session['uid']=user.id
                login(request,user)
                err='no' 
                return redirect('/admin_home')                
        except:
            err='yes'                                
    return render(request,'users/index.html',locals())



def Admin_home(request):
    lst=[]
    ut=0
    u=My_Upload_file.objects.all()
    pm=PM.objects.all()
    qc=Qc_user.objects.all()
    ed=ED_User.objects.all()
    data={'ht':u,'pm':pm,'qc':qc,'ed':ed}      
    try:   # print(pm_data)         
        if request.method=='POST':             
            fsh=request.FILES.get('file')
            seg=request.POST.get('seg')
            u=My_Upload_file()
            u.file=fsh
            u.seg=seg
            u.save()
            f=open(f'{settings.BASE_DIR}//{fsh}','r')
            f1=json.load(f)
            st=len(f1)-1 
            count=len(f1)   
            # print(count)            
            u.count=count
            for i in f1: 
                d=(i['Published_Date']) 
                lst.append(d)
            da=[]
            for i in lst:
                date_str =i
                datetime_object = datetime.strptime(date_str,'%Y-%m-%d')
                date_object = datetime_object.date()
                # print(date_object)
                da.append(date_object)
                # print(da)
            # print(da)
            dt=sorted(da)
            from_date=dt[ut]
            to_date=dt[st]
            # print(from_date)
            # print(to_date)
            u.from_date=from_date
            u.to_date=to_date                    
            u.save() 
    except:                    
        return redirect('/admin_home')    
        # return HttpResponse('error')  
    return render(request,'users/admin_home.html',data)




def View_file(request,id):
    lst=[]
    d=[]
    d1=[]
    ut=0    
    u=My_Upload_file.objects.all()    
    files=''
    u1=My_Upload_file.objects.filter(id=id)   
    for i in u1:
       files=i.file
       seg=i.seg

    if seg == 'rc':       
        f=open(f'{settings.BASE_DIR}//{files}','r')
        f1=json.load(f) 
        data=(f1[0].keys())
        for i in data:
           d.append(i)


    elif seg =='pnf':
        f=open(f'{settings.BASE_DIR}//{files}','r')
        f1=json.load(f) 
        data=(f1[0].keys())
        for i in data:
           d1.append(i)

    # print(d)
    st=len(f1)-1 
    for i in f1: 
        da=(i['Published_Date'])    
        lst.append(da)
    da=[]
    for i in lst:
        date_str =i
        datetime_object = datetime.strptime(date_str,'%Y-%m-%d')
        date_object = datetime_object.date()
        da.append(date_object)
        dt=sorted(da)
    from_date=dt[ut]
    to_date=dt[st]
   
    data={'data':f1,'ua':u,'ht':seg,'d':d,'f':from_date,'t':to_date,'d1':d1}   
    return render(request,'users/view_files.html',locals())




def Push_to_pm(request,pid):
    u=My_Upload_file.objects.get(id=pid) 
    pd=Push_to_pm_file()
    pd.my_file=u 
    # pd.save()
    u.status=True
    u.save()
    pd.save()

    return redirect('/admin_home')




def Delete(request,id):
    u=My_Upload_file.objects.filter(id=id)   
    u.delete()
    return redirect('/admin_home') 




def Logout_user(request):
    logout(request)
    return redirect('/')



def Make_pm(request):
    err=''
    if request.method=='POST':
        f_n=request.POST.get('f_n')
        l_n=request.POST.get('l_n')  
        email=request.POST.get('email')
        p=request.POST.get('p')
        try:
            user=User.objects.create_user(first_name=f_n,last_name=l_n,username=email,password=p)
            PM.objects.create(user=user)
            err='no'
            return redirect('/admin_home')
        except:
            err='yes'    
    return render(request,'pm/make_pm.html')




def PM_login(request):
    if request.method=='POST':
        u=request.POST.get('email')
        p=request.POST.get('p')
        user=authenticate(User,username=u,password=p)
        try:
            if user  is not None:
                request.session['uid']=user.id
                login(request,user)
                err='no'
                return redirect('/pm_home')
        except:
            err='yes' 
    return render(request,'pm/pm_login.html',locals())


def PM_home(request):
    qc_data=my_Qc_data.objects.all()
    p=Push_to_pm_file.objects.all()
    fd=Final_data_PM.objects.all()
    data={'p':p,'dt':qc_data,'fd':fd}
    return render(request,'pm/pm_home.html',data)


def PM_view_file(request,id):
    edi=0    
    u=Push_to_pm_file.objects.get(id=id) 
    u1=Push_to_pm_file.objects.filter(id=id)    
    ac=Add_col.objects.filter(file_id=u)
    for k in ac:
        edi=k.eid
    for i in u1:      
        pid=i.id
        files=i.my_file.file
    f=open(f'{settings.BASE_DIR}//{files}','r') 
    f1=json.load(f)
    if request.method=='POST':
        col=request.POST.get('col')
        data1=request.POST.get('data')
        v=request.POST.get('v')
        a_c= Add_col()
        a_c.eid=v
        a_c.file=u
        a_c.st=True
        a_c.save()
        data={col:data1}
        for i in f1:
            i.update(data)
        f=open(f'{settings.BASE_DIR}//{files}','w')   
        json.dump(f1,f)  
        data={'col':col,'d':data1}
        return redirect('/pm_home')

    lst=[]
    d=[]
    d1=[]
    ut=0    
    u=Push_to_pm_file.objects.all()    
    files=''
    u1=Push_to_pm_file.objects.filter(id=id)   
    for i in u1:
       files=i.my_file.file
       seg=i.my_file.seg
    # print(seg)

    if seg == 'rc':       
        f=open(f'{settings.BASE_DIR}//{files}','r')
        f1=json.load(f) 
        data=(f1[0].keys())
        for i in data:
           d.append(i)


    elif seg =='pnf':
        f=open(f'{settings.BASE_DIR}//{files}','r')
        f1=json.load(f) 
        data=(f1[0].keys())
        for i in data:
           d1.append(i)

    # print(d)
    st=len(f1)-1 
    for i in f1: 
        da=(i['Published_Date'])    
        lst.append(da)
    da=[]
    for i in lst:
        date_str =i
        datetime_object = datetime.strptime(date_str,'%Y-%m-%d')
        date_object = datetime_object.date()
        da.append(date_object)
        dt=sorted(da)
    from_date=dt[ut]
    to_date=dt[st]
   
    data={'data':f1,'ua':u,'ht':seg,'d':d,'f':from_date,'t':to_date,'d1':d1,'eid':edi}   
    return render(request,'pm/pm_view_files.html',locals())

def PM_file_delete(request,id):
    u=Push_to_pm_file.objects.filter(id=id)   
    u.delete()
    return redirect('/pm_home') 


def Push_to_qc(request,id):
    u=Push_to_pm_file.objects.get(id=id)  
    # print(u.my_file) 
    st=0    
    if request.method=='POST':
        u1=Push_to_pm_file.objects.filter(id=id)
        for i in u1:
           files=i.my_file.file  
          
        #    print(files)   
        f=open(f'{settings.BASE_DIR}//{files}','r')
        f1=json.load(f)
    
        cf=request.POST.get('file_name')
        user1=request.POST.get('user')
        user=User.objects.get(id=user1)
       
        # print(user)
        en=request.POST.get('end')
        strt=request.POST.get('start')
        msg=request.POST.get('msg')
        # # print(en)
        first=int(strt)-1
        last=int(en)-1
        # print(first)
        # print(last)
        new_file=f1[first:last]
        file=open(f'{settings.BASE_DIR}//{cf}'+'.json','w')
        json.dump(new_file,file)
        f3=open(f'{settings.BASE_DIR}//{files}','r')
        f2=json.load(f3)
        del f2[first:last]
        try:
            qc=my_Qc_data()
            qc.user=user
            qc.my_file=u
            qc.qc_file=cf+'.json'
            qc.end=en
            qc.start=strt
            qc.msg=msg
            qc.save()        
            return redirect('/pm_home')
        except:
            return HttpResponse('error')
    else:  
        fr=qc_Form()
        fr1={"form":fr}    
        return render(request,'pm/push_to_qc.html',fr1)  







def Make_qc(request):
    err=''
    if request.method=='POST':
        un=request.POST.get('un')
        f_n=request.POST.get('f_n')
        l_n=request.POST.get('l_n')  
        email=request.POST.get('email')
        p=request.POST.get('p')
        try:
            user=User.objects.create_user(first_name=f_n,last_name=l_n,email=email,username=un,password=p)
            Qc_user.objects.create(user=user)
            err='no'
            
            return redirect('/admin_home')
        except:
            err='yes'
    return render(request,'qc/make_qc.html')



def QC_login(request):
    if request.method=='POST':
        u=request.POST.get('email')
        p=request.POST.get('p')
        user=authenticate(User,username=u,password=p)
        try:
            if user  is not None:
                request.session['uid']=user.id
                login(request,user)
                err='no'
                return redirect('/qc_home')
        except:
            err='yes' 
    return render(request,'qc/qc_login.html')




def QC_home(request):
    pid=request.session.get('uid')
    data=my_Qc_data.objects.filter(user=pid)
    # for i in data:
    #     print(i.my_file.my_file.seg)    
    d={'dat':data}
    # print(d)
    return render(request,'qc/qc_home.html',d)



def QC_view_file(request,id):
    edi=0
    dat=''    
    u=my_Qc_data.objects.get(id=id) 
    u1=my_Qc_data.objects.filter(id=id)    
    ac=Add_col_qc.objects.filter(file_id=u)
    for k in ac:
        
        dat=k.data
    for i in u1:      
        pid=i.id
        files=i.qc_file
    f=open(f'{settings.BASE_DIR}//{files}','r') 
    f1=json.load(f)
    if request.method=='POST':
        col=request.POST.get('col')
        data1=request.POST.get('data')
        v=request.POST.get('v')
        a_c= Add_col_qc()
        # a_c.eid=v
        a_c.data=data1
        a_c.col=col
        a_c.file=u
        a_c.st=True
        a_c.save()
        data={col:data1}
        for i in f1:
            i.update(data)
        f=open(f'{settings.BASE_DIR}//{files}','w')   
        json.dump(f1,f)  
        data={'col':col,'dat':dat,'ac':ac}
        return redirect('/qc_home')



    lst=[]
    d=[]
    d1=[]
    ut=0    
    
    u=my_Qc_data.objects.all()    
    files=''
    u1=my_Qc_data.objects.filter(id=id)   
    for i in u1:
       files=i.qc_file
       seg=i.my_file.my_file.seg
    # print(seg)

    if seg == 'rc':       
        f=open(f'{settings.BASE_DIR}//{files}','r')
        f1=json.load(f) 
        data=(f1[0].keys())
        for i in data:
           d.append(i)


    elif seg =='pnf':
        f=open(f'{settings.BASE_DIR}//{files}','r')
        f1=json.load(f) 
        data=(f1[0].keys())
        for i in data:
           d1.append(i)

    # print(d)
    st=len(f1)-1 
    for i in f1: 
        da=(i['Published_Date']) 
        # print(da)   
        lst.append(da)
    da=[]
    for i in lst:
        date_str =i
        datetime_object = datetime.strptime(date_str,'%Y-%m-%d')
        date_object = datetime_object.date()
        da.append(date_object)
        dt=sorted(da)
    from_date=dt[ut]
    to_date=dt[st]
   
    data={'data':f1,'ua':u,'ht':seg,'d':d,'f':from_date,'t':to_date,'d1':d1}   
    return render(request,'qc/qc_view_files.html',locals())


# def QC_edit_file(request,id):
    lst=[]
    d=[]
    d1=[]
    ut=0    
    u=my_Qc_data.objects.all()    
    files=''
    u1=my_Qc_data.objects.filter(id=id)   
    for i in u1:
       pid=i.id
       files=i.qc_file
       seg=i.my_file.my_file.seg
    # print(pid)
    
    # print(seg)

    if seg == 'rc':       
        f=open(f'{settings.BASE_DIR}//{files}','r')
        f1=json.load(f) 
        data=(f1[0].keys())
        for i in data:
           d.append(i)


    elif seg =='pnf':
        f=open(f'{settings.BASE_DIR}//{files}','r')
        f1=json.load(f) 
        data=(f1[0].keys())
        for i in data:
           d1.append(i)

    # print(d)
    st=len(f1)-1 
    for i in f1: 
        da=(i['Published_Date']) 
        # print(da)   
        lst.append(da)
    da=[]
    for i in lst:
        date_str =i
        datetime_object = datetime.strptime(date_str,'%Y-%m-%d')
        date_object = datetime_object.date()
        da.append(date_object)
        dt=sorted(da)
    from_date=dt[ut]
    to_date=dt[st]
   
    data={'data':f1,'ua':u,'ht':seg,'d':d,'f':from_date,'t':to_date,'d1':d1,'fr':pid}   
    return render(request,'qc/qc_edit.html',locals()) 

def QC_Edit_data(request,pid,did):
    col=''
    upid=request.session.get('uid')
    user=User.objects.get(id=upid)
    u1=my_Qc_data.objects.get(id=pid)
    u=my_Qc_data.objects.filter(id=pid) 
    ac=Add_col_qc.objects.filter(file_id=u1) 
    for i in ac:
        print(i.file.qc_file)
        col=i.col
    for i in u:
        files=i.qc_file  
        seg=i.my_file.my_file.seg

    try:
        if seg == 'rc':
            if request.method=='POST':
                sr_no=request.POST.get('sr_no')
                sheet=request.POST.get('sheet_no')
                p_date=request.POST.get('p_date')
                r_body=request.POST.get('r_body')
                title=request.POST.get('title')
                url=request.POST.get('url')
                res=request.POST.get('res')
                date=request.POST.get('date')
                w_s=request.POST.get('w_s')
                d_s=request.POST.get('d_s')
                r_s=request.POST.get('r_s')
                rule=request.POST.get('rule')
                country=request.POST.get('country')
                sector=request.POST.get('sector')
                impact=request.POST.get('impact')
                w_a=request.POST.get('w_a')
                Timeline=request.POST.get('time')
                c_d=request.POST.get('c_d')
                e_i=request.POST.get('e_i')
                act=request.POST.get('act')
                section=request.POST.get('section')
                s_r=request.POST.get('s_r')
                d_a=request.POST.get('d_a')
                n_p=request.POST.get('n_p')
                r_d=request.POST.get('r_d')
                qc_c=request.POST.get('qc_c')
                f_d=request.POST.get('f_d')
                qc_s=request.POST.get('qc_s')
                n_art=request.POST.get('n_art')
                new_col=request.POST.get('new_col')
        
                u=my_Qc_data.objects.filter(id=pid)   
                for i in u:
                    files=i.qc_file  
                    seg=i.my_file.my_file.seg     
                f=open(f'{settings.BASE_DIR}//{files}','r')
                f1=json.load(f)
                f1[did]['Sr_No']=sr_no
                f1[did]['Sheet_No']=sheet
                f1[did]['Published_Date']=p_date
                f1[did]['Regulatory_Body']=r_body
                f1[did]['Title']=title
                f1[did]['URL']=url
                f1[did]['Researcher']=res
                f1[did]['Date']=date
                f1[did]['Working_Status']= w_s
                f1[did]['Document_Status']=d_s
                f1[did]['Rules_Status']=r_s
                f1[did]['Rule']=rule
                f1[did]['Country']=country
                f1[did]['Sector']=sector
                f1[did]['Impact']=impact
                f1[did]['What_is_this_about']=w_a
                f1[did]['Timeline']=Timeline
                f1[did]['Compliance_date']=c_d
                f1[did]['Entities_Impacted']=e_i
                f1[did]['Act']=act
                f1[did]['Section']=section
                f1[did]['Summary_Remarks']=s_r
                f1[did]['Description_Automated']=d_a
                f1[did]['NEW_Prompt']=n_p
                f1[did]['Researcher_Doubt']=r_d
                f1[did]['QC_Comments']=qc_c
                f1[did]['Final_Description']=f_d
                f1[did]['QC_status']=qc_s
                f1[did]['Notes_on_article']= n_art
                f1[did][f'{col}']=new_col
                
                
            
                f=open(f'{settings.BASE_DIR}//{files}','w')
                json.dump(f1,f)   
                return redirect('/qc_home')
                    
            else:
                u=my_Qc_data.objects.filter(id=pid)   
                for i in u:
                   files=i.qc_file
                   ui=i.id
                fr=ui       
                f=open(f'{settings.BASE_DIR}//{files}','r')
                f1=json.load(f) 
                sr_no=f1[did]['Sr_No']
                sheet=f1[did]['Sheet_No']
                p_date=f1[did]['Published_Date']
                r_body=f1[did]['Regulatory_Body']
                title=f1[did]['Title']
                url=f1[did]['URL']
                res=f1[did]['Researcher']
                date=f1[did]['Date']
                w_s=f1[did]['Working_Status']
                d_s=f1[did]['Document_Status']
                r_s=f1[did]['Rules_Status']
                rule=f1[did]['Rule']
                country=f1[did]['Country']
                sector=f1[did]['Sector']
                impact=f1[did]['Impact']
                w_a=f1[did]['What_is_this_about']
                Timeline=f1[did]['Timeline']
                c_d=f1[did]['Compliance_date']
                e_i=f1[did]['Entities_Impacted']
                act=f1[did]['Act']
                section=f1[did]['Section']
                s_r=f1[did]['Summary_Remarks']
                d_a=f1[did]['Description_Automated']
                n_p=f1[did]['NEW_Prompt']
                r_d=f1[did]['Researcher_Doubt']
                qc_c=f1[did]['QC_Comments']
                f_d=f1[did]['Final_Description']
                qc_s=f1[did]['QC_status']
                n_art=f1[did]['Notes_on_article']
                new_col=f1[did][f'{col}']
                
                

        elif seg == 'pnf':
            if request.method=='POST':
                sr_no=request.POST.get('sr_no')
                u_r_i=request.POST.get('u_r_i')
                r_n=request.POST.get('r_n')
                sheet=request.POST.get('sheet_no')
                url=request.POST.get('url')
                r_body=request.POST.get('r_body')
                p_date=request.POST.get('p_date')
                title=request.POST.get('title')
                article=request.POST.get('article')
                type=request.POST.get('type')
                res=request.POST.get('res')
                date=request.POST.get('date')
                status=request.POST.get('status')
                case_status=request.POST.get('case_status')
                order_type=request.POST.get('order')
                imposed_value=request.POST.get('i_v')
                settled_value=request.POST.get('s_v')
                currency=request.POST.get('curr')
                cause_of_penalty=request.POST.get('c_o_f')
                activity=request.POST.get('act')
                entity_status=request.POST.get('e_s')
                company=request.POST.get('c_name')
                individual_name=request.POST.get('i_name')
                industry=request.POST.get('ind')
                third_parties=request.POST.get('t_p')
                s_r=request.POST.get('s_r')
                d_a=request.POST.get('d_a')
                r_d=request.POST.get('r_d')
                qc_c=request.POST.get('qc_c')
                f_d=request.POST.get('f_d')
                qc_s=request.POST.get('qc_s')
                n_art=request.POST.get('n_art')
                new_col=request.POST.get('new_col')

                u=my_Qc_data.objects.filter(id=pid)   
                for i in u:
                    files=i.qc_file  
                    seg=i.my_file.my_file.seg     
                f=open(f'{settings.BASE_DIR}//{files}','r')
                f1=json.load(f) 
                f1[did]['Sr_No']=sr_no
                f1[did]['Unique_REC_ID']=u_r_i
                f1[did]['Rec_No']=r_n
                f1[did]['Sheet_No']=sheet
                f1[did]['URL']=url
                f1[did]['Regulatory']=r_body
                f1[did]['Published_Date']=p_date
                f1[did]['Title']= title
                f1[did]['Article']=article
                f1[did]['Type']=type
                f1[did]['Researcher']=res
                f1[did]['Working_Date']=date
                f1[did]['Status']=status
                f1[did]['Case_Status']=case_status
                f1[did]['Order_Type']=order_type
                f1[did]['Imposed_Value']=imposed_value
                f1[did]['Settled_Value']=settled_value
                f1[did]['Currency']=currency
                f1[did]['Cause_of_Penalty']=cause_of_penalty
                f1[did]['Registered_Unregistered_activity']=activity
                f1[did]['Entity_Status']=entity_status
                f1[did]['Company_Name']=company
                f1[did]['Individual_Name']=individual_name
                f1[did]['Industry']=industry
                f1[did]['Third_parties']=third_parties
                f1[did]['Summary_Remarks']=s_r
                f1[did]['Description_Automated']=d_a
                f1[did]['Researcher_Doubts']=r_d
                f1[did]['QC_Comments']=qc_c
                f1[did]['Final_Description']=f_d
                f1[did]['QC_Status']=qc_s
                f1[did]['Notes_on_Article_History']=n_art
                f1[did][f'{col}']=new_col
                f=open(f'{settings.BASE_DIR}//{files}','w')
                json.dump(f1,f)   
                return redirect('/qc_home')
                    
            else:
                u=my_Qc_data.objects.filter(id=pid)   
                for i in u:
                   files=i.qc_file
                   ui=i.id
                fr=ui       
                f=open(f'{settings.BASE_DIR}//{files}','r')
                f1=json.load(f)  
                sr_no=f1[did]['Sr_No']
                unique_rec_id=f1[did]['Unique_REC_ID']
                rec_no=f1[did]['Rec_No']
                sheet=f1[did]['Sheet_No']
                url=f1[did]['URL']
                regulatory=f1[did]['Regulatory']
                p_date=f1[did]['Published_Date']
                title=f1[did]['Title']
                article=f1[did]['Article']
                type=f1[did]['Type']
                res=f1[did]['Researcher']
                date=f1[did]['Working_Date']
                status=f1[did]['Status']
                case_status=f1[did]['Case_Status']
                order=f1[did]['Order_Type']
                i_v=f1[did]['Imposed_Value']
                s_v=f1[did]['Settled_Value']
                curr=f1[did]['Currency']
                c_o_p=f1[did]['Cause_of_Penalty']
                act=f1[did]['Registered_Unregistered_activity']
                e_s=f1[did]['Entity_Status']
                c_name=f1[did]['Company_Name']
                i_name=f1[did]['Individual_Name']
                ind=f1[did]['Industry']
                t_p=f1[did]['Third_parties']
                s_r=f1[did]['Summary_Remarks']
                d_a=f1[did]['Description_Automated']
                r_d=f1[did]['Researcher_Doubts']
                qc_c=f1[did]['QC_Comments']
                f_d=f1[did]['Final_Description']
                qc_s=f1[did]['QC_Status']
                n_art=f1[did]['Notes_on_Article_History']
                new_col=f1[did][f'{col}']
    except:
        return redirect('/qc_home')
               

    return render(request,'qc/qc_edit_form.html',locals()) 



def Make_ed(request):
    if request.method=='POST':
        un=request.POST.get('un')
        f_n=request.POST.get('f_n')
        l_n=request.POST.get('l_n')  
        email=request.POST.get('email')
        p=request.POST.get('p')
        try:
            user=User.objects.create_user(first_name=f_n,last_name=l_n,email=email,username=un,password=p)
            ED_User.objects.create(user=user)
           
            return redirect('/admin_home')
        except:
            err='yes'
    return render(request,'ed/make_ed.html')




def Push_to_Ed(request,id):
    upid=request.session.get('uid')
    user=Qc_user.objects.get(user=upid)
    
    if request.method=='POST':
        ed=request.POST.get('Ed')
        ed_ed=ED_User.objects.get(id=ed)
        # qc_data1=request.POST.get('qc_data')
        qc_data=my_Qc_data.objects.get(id=id)  
        qc_data.status=True 
        try:
            ed_push=Editor_push()
            ed_push.Ed=ed_ed
            ed_push.qc_data=qc_data
            ed_push.qc_user=user

            ed_push.save()
            qc_data.save()
            return redirect('/qc_home')
        except:
            fr=pushForm()
            f={"form":fr}
            return render(request,'ed/push_to_ed.html',f)       
    else:
        fr=pushForm()
        f={"form":fr}
        return render(request,'ed/push_to_ed.html',f)
    


def ED_login(request):
    if request.method=='POST':
        u=request.POST.get('un')
        p=request.POST.get('p')
        user=authenticate(User,username=u,password=p)
        try:
            if user  is not None:
                request.session['uid']=user.id
                login(request,user)
                err='no'
                return redirect('/ed_home')
        except:
            err='yes' 
    return render(request,'ed/ed_login.html')



def ED_home(request):
    upid=request.session.get('uid')
    e=ED_User.objects.get(user_id=upid)
    eid=e.id
    ed_data=Editor_push.objects.filter(Ed=eid)
    dat=Final_data_PM.objects.filter(editior_id=eid)
    
        
    for i in ed_data:
        i.qc_data.my_file.my_file

    d={'dat':ed_data,'dt':dat}
    
    return render(request,'ed/ed_home.html',d)



def ED_view_file(request,id):
    lst=[]
    d=[]
    d1=[]
    ut=0  
    fd=0  
    dat=''
    col=''
    u=Editor_push.objects.all()    
    files=''
    u1=Editor_push.objects.filter(id=id) 
     
    # ac=Add_col_qc.objects.filter(file_id=u1)  
    for i in u1:
       fr=i.id
       files=i.qc_data.qc_file
       fd=i.qc_data_id
    #    print(fd)
       seg=i.qc_data.my_file.my_file.seg
    ac=Add_col_qc.objects.filter(file_id=fd)
    for i in ac:
        dat=i.data 
        col=i.col 
    # print(seg,files)

    if seg == 'rc':       
        f=open(f'{settings.BASE_DIR}//{files}','r')
        f1=json.load(f) 
        data=(f1[0].keys())
        for i in data:
           d.append(i)


    elif seg =='pnf':
        f=open(f'{settings.BASE_DIR}//{files}','r')
        f1=json.load(f) 
        data=(f1[0].keys())
        for i in data:
           d1.append(i)

    # print(d)
    st=len(f1)-1 
    for i in f1: 
        da=(i['Published_Date']) 
        # print(da)   
        lst.append(da)
    da=[]
    for i in lst:
        date_str =i
        datetime_object = datetime.strptime(date_str,'%Y-%m-%d')
        date_object = datetime_object.date()
        da.append(date_object)
        dt=sorted(da)
    from_date=dt[ut]
    to_date=dt[st]
   
    data={'data':f1,'ua':u,'ht':seg,'d':d,'f':from_date,'t':to_date,'d1':d1,'pid':fr,'dat':dat,'col':col}   
    return render(request,'ed/ed_view_file.html',locals())


def ED_Edit_data(request,pid,did):
    dat=''
    col=''
    upid=request.session.get('uid')
    user=User.objects.get(id=upid)
    u=Editor_push.objects.filter(id=pid)   
    for i in u:
        files=i.qc_data.qc_file
        seg=i.qc_data.my_file.my_file.seg
        fd=i.qc_data_id
    ac=Add_col_qc.objects.filter(file_id=fd)
    for i in ac:
        dat=i.data
        col=i.col  
    try:
        if seg == 'rc':
            if request.method=='POST':
                sr_no=request.POST.get('sr_no')
                sheet=request.POST.get('sheet_no')
                p_date=request.POST.get('p_date')
                r_body=request.POST.get('r_body')
                title=request.POST.get('title')
                url=request.POST.get('url')
                res=request.POST.get('res')
                date=request.POST.get('date')
                w_s=request.POST.get('w_s')
                d_s=request.POST.get('d_s')
                r_s=request.POST.get('r_s')
                rule=request.POST.get('rule')
                country=request.POST.get('country')
                sector=request.POST.get('sector')
                impact=request.POST.get('impact')
                w_a=request.POST.get('w_a')
                Timeline=request.POST.get('time')
                c_d=request.POST.get('c_d')
                e_i=request.POST.get('e_i')
                act=request.POST.get('act')
                section=request.POST.get('section')
                s_r=request.POST.get('s_r')
                d_a=request.POST.get('d_a')
                n_p=request.POST.get('n_p')
                r_d=request.POST.get('r_d')
                qc_c=request.POST.get('qc_c')
                f_d=request.POST.get('f_d')
                qc_s=request.POST.get('qc_s')
                n_art=request.POST.get('n_art')
                new_col=request.POST.get('new_col')
        
                u=Editor_push.objects.filter(id=pid)   
                for i in u:
                    files=i.qc_data.qc_file
                    seg=i.qc_data.my_file.my_file.seg    
                f=open(f'{settings.BASE_DIR}//{files}','r')
                f1=json.load(f)
                f1[did]['Sr_No']=sr_no
                f1[did]['Sheet_No']=sheet
                f1[did]['Published_Date']=p_date
                f1[did]['Regulatory_Body']=r_body
                f1[did]['Title']=title
                f1[did]['URL']=url
                f1[did]['Researcher']=res
                f1[did]['Date']=date
                f1[did]['Working_Status']= w_s
                f1[did]['Document_Status']=d_s
                f1[did]['Rules_Status']=r_s
                f1[did]['Rule']=rule
                f1[did]['Country']=country
                f1[did]['Sector']=sector
                f1[did]['Impact']=impact
                f1[did]['What_is_this_about']=w_a
                f1[did]['Timeline']=Timeline
                f1[did]['Compliance_date']=c_d
                f1[did]['Entities_Impacted']=e_i
                f1[did]['Act']=act
                f1[did]['Section']=section
                f1[did]['Summary_Remarks']=s_r
                f1[did]['Description_Automated']=d_a
                f1[did]['NEW_Prompt']=n_p
                f1[did]['Researcher_Doubt']=r_d
                f1[did]['QC_Comments']=qc_c
                f1[did]['Final_Description']=f_d
                f1[did]['QC_status']=qc_s
                f1[did]['Notes_on_article']= n_art
                f1[did][f'{col}']=new_col
            
                f=open(f'{settings.BASE_DIR}//{files}','w')
                json.dump(f1,f)   
                return redirect('/ed_home')
                    
            else:
                did=did
                u=Editor_push.objects.filter(id=pid)   
                for i in u:
                    ui=i.id
                    files=i.qc_data.qc_file
                    seg=i.qc_data.my_file.my_file.seg
                fr=ui       
                f=open(f'{settings.BASE_DIR}//{files}','r')
                f1=json.load(f) 
                sr_no=f1[did]['Sr_No']
                sheet=f1[did]['Sheet_No']
                p_date=f1[did]['Published_Date']
                r_body=f1[did]['Regulatory_Body']
                title=f1[did]['Title']
                url=f1[did]['URL']
                res=f1[did]['Researcher']
                date=f1[did]['Date']
                w_s=f1[did]['Working_Status']
                d_s=f1[did]['Document_Status']
                r_s=f1[did]['Rules_Status']
                rule=f1[did]['Rule']
                country=f1[did]['Country']
                sector=f1[did]['Sector']
                impact=f1[did]['Impact']
                w_a=f1[did]['What_is_this_about']
                Timeline=f1[did]['Timeline']
                c_d=f1[did]['Compliance_date']
                e_i=f1[did]['Entities_Impacted']
                act=f1[did]['Act']
                section=f1[did]['Section']
                s_r=f1[did]['Summary_Remarks']
                d_a=f1[did]['Description_Automated']
                n_p=f1[did]['NEW_Prompt']
                r_d=f1[did]['Researcher_Doubt']
                qc_c=f1[did]['QC_Comments']
                f_d=f1[did]['Final_Description']
                qc_s=f1[did]['QC_status']
                n_art=f1[did]['Notes_on_article']
                new_col=f1[did][f'{col}'] 

        elif seg == 'pnf':
            if request.method=='POST':
                sr_no=request.POST.get('sr_no')
                u_r_i=request.POST.get('u_r_i')
                r_n=request.POST.get('r_n')
                sheet=request.POST.get('sheet_no')
                url=request.POST.get('url')
                r_body=request.POST.get('r_body')
                p_date=request.POST.get('p_date')
                title=request.POST.get('title')
                article=request.POST.get('article')
                type=request.POST.get('type')
                res=request.POST.get('res')
                date=request.POST.get('date')
                status=request.POST.get('status')
                case_status=request.POST.get('case_status')
                order_type=request.POST.get('order')
                imposed_value=request.POST.get('i_v')
                settled_value=request.POST.get('s_v')
                currency=request.POST.get('curr')
                cause_of_penalty=request.POST.get('c_o_f')
                activity=request.POST.get('act')
                entity_status=request.POST.get('e_s')
                company=request.POST.get('c_name')
                individual_name=request.POST.get('i_name')
                industry=request.POST.get('ind')
                third_parties=request.POST.get('t_p')
                s_r=request.POST.get('s_r')
                d_a=request.POST.get('d_a')
                r_d=request.POST.get('r_d')
                qc_c=request.POST.get('qc_c')
                f_d=request.POST.get('f_d')
                qc_s=request.POST.get('qc_s')
                n_art=request.POST.get('n_art')
                new_col=request.POST.get('new_col')

                u=Editor_push.objects.filter(id=pid)   
                for i in u:
                    files=i.qc_data.qc_file
                    seg=i.qc_data.my_file.my_file.seg    
                f=open(f'{settings.BASE_DIR}//{files}','r')
                f1=json.load(f) 
                f1[did]['Sr_No']=sr_no
                f1[did]['Unique_REC_ID']=u_r_i
                f1[did]['Rec_No']=r_n
                f1[did]['Sheet_No']=sheet
                f1[did]['URL']=url
                f1[did]['Regulatory']=r_body
                f1[did]['Published_Date']=p_date
                f1[did]['Title']= title
                f1[did]['Article']=article
                f1[did]['Type']=type
                f1[did]['Researcher']=res
                f1[did]['Working_Date']=date
                f1[did]['Status']=status
                f1[did]['Case_Status']=case_status
                f1[did]['Order_Type']=order_type
                f1[did]['Imposed_Value']=imposed_value
                f1[did]['Settled_Value']=settled_value
                f1[did]['Currency']=currency
                f1[did]['Cause_of_Penalty']=cause_of_penalty
                f1[did]['Registered_Unregistered_activity']=activity
                f1[did]['Entity_Status']=entity_status
                f1[did]['Company_Name']=company
                f1[did]['Individual_Name']=individual_name
                f1[did]['Industry']=industry
                f1[did]['Third_parties']=third_parties
                f1[did]['Summary_Remarks']=s_r
                f1[did]['Description_Automated']=d_a
                f1[did]['Researcher_Doubts']=r_d
                f1[did]['QC_Comments']=qc_c
                f1[did]['Final_Description']=f_d
                f1[did]['QC_Status']=qc_s
                f1[did]['Notes_on_Article_History']=n_art
                f1[did][f'{col}']=new_col
                f=open(f'{settings.BASE_DIR}//{files}','w')
                json.dump(f1,f)   
                return redirect('/ed_home')
                    
            else:
                did=did
                u=Editor_push.objects.filter(id=pid)   
                for i in u:
                    ui=i.id
                    files=i.qc_data.qc_file
                    seg=i.qc_data.my_file.my_file.seg
                fr=ui       
                f=open(f'{settings.BASE_DIR}//{files}','r')
                f1=json.load(f)  
                sr_no=f1[did]['Sr_No']
                unique_rec_id=f1[did]['Unique_REC_ID']
                rec_no=f1[did]['Rec_No']
                sheet=f1[did]['Sheet_No']
                url=f1[did]['URL']
                regulatory=f1[did]['Regulatory']
                p_date=f1[did]['Published_Date']
                title=f1[did]['Title']
                article=f1[did]['Article']
                type=f1[did]['Type']
                res=f1[did]['Researcher']
                date=f1[did]['Working_Date']
                status=f1[did]['Status']
                case_status=f1[did]['Case_Status']
                order=f1[did]['Order_Type']
                i_v=f1[did]['Imposed_Value']
                s_v=f1[did]['Settled_Value']
                curr=f1[did]['Currency']
                c_o_p=f1[did]['Cause_of_Penalty']
                act=f1[did]['Registered_Unregistered_activity']
                e_s=f1[did]['Entity_Status']
                c_name=f1[did]['Company_Name']
                i_name=f1[did]['Individual_Name']
                ind=f1[did]['Industry']
                t_p=f1[did]['Third_parties']
                s_r=f1[did]['Summary_Remarks']
                d_a=f1[did]['Description_Automated']
                r_d=f1[did]['Researcher_Doubts']
                qc_c=f1[did]['QC_Comments']
                f_d=f1[did]['Final_Description']
                qc_s=f1[did]['QC_Status']
                n_art=f1[did]['Notes_on_Article_History'] 
                new_col=f1[did][f'{col}'] 
    except:
        return redirect('/ed_home')          

    return render(request,'ed/ed_edit_form.html',locals()) 

def ED_send_file(request,id):
    upid=request.session.get('uid')
    user=ED_User.objects.get(user=upid)
    ed_push=Editor_push.objects.get(id=id)
    if request.method=='POST':
        pm1=request.POST.get('pm')
        pm=PM.objects.get(id=pm1)
        ed_push.sta=True
        # print(ed_push,pm,seg,msg,user)
        try:

            f=Final_data_PM()
            f.pm=pm       
            f.Edited_file=ed_push
            f.editior=user
            f.status=True
            
            ed_push.save()
            f.save()
            
            return redirect('/ed_home')
        except:
            return redirect('/ed_home')
       
    else:
        fr=Final_form()
        f={'form':fr}
        return render(request,'ed/ed_send_form.html',f)


def Download_file(request,id):
    files=''
    name=''

    fd=Final_data_PM.objects.filter(id=id)
    for i in fd:
        files=i.Edited_file.qc_data.qc_file
        name=i.Edited_file.qc_data.qc_file.name
    name=name[0:5]
    try:

        with open(f'{settings.BASE_DIR}//{files}','r') as f:   
           pd.read_json(f).to_excel(f'C://Excle_files//{name}.xlsx')
        messages.success(request,'Your File is Download')

    except:
        messages.warning(request,'Somethig Went Wrong')    

    return redirect('/pm_home')

def About(request):
    return render(request,'users/about.html')





