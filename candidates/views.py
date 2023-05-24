from django.shortcuts import render
from .models import Job





def job_search_list(request):
    query=request.GET.get('p')
    loc = request.GET.get('q')
    object_list=[]
    
    if(query == None):
        object_list= Job.objects.all
    else :
        title_list=Job.objects.filter(title__icontains=query).order_by('date_posted')
        skill_list=Job.objects.filter(skill_req__icontains=query).order_by('date_posted')
        job_type_list=Job.objects.filter(job_type__icontains=query).order_by('date_posted')
        company_list=Job.objects.filter(company__icontains==query).order_by('-date_posted')
        for i in title_list:
            object_list.append(i)
        for i in skill_list:
            if i not in object_list:
                object_list.append(i)
        for i in job_type_list:
            if i not in object_list:
                object_list.append(i)
        for i in company_list:
            if i not in object_list:
                object_list.append(i)
        
        if (loc == None):
            location= Job.objects.all()
        else:
            location=Job.objects.filter(location__icontains=loc).order_by('date_posted')
        final_list=[]
        
        for i in object_list:
            if i in location:
                final_list.append(i)
                
        paginator= Paginator(final_list,20)
        page_number= request.GET.get('page')
        page_obj=paginator.get_page(page_number)
         
    