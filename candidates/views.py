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
        company_list=Job.objects.filter(job_type__icontains==query).order_by('-date_posted')
        
        