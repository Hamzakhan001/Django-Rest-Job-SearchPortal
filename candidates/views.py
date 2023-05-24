from django.shortcuts import render
from .models import AppliedJobs,Profile,SavedJobs,Skill
from .forms import ProfileUpdateForm, NewSkillForm




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
        
        context={
			'jobs':page_obj,
			'query':query
		}
        
        return render(request, 'candidates/job_search_list.html',context)
        
         
def job_detail(request,slug):
    job=get_object_or_404(Job, slug=slug)
    apply_btn=0
    save_btn=0
    
    profile=Profile.object.filter(user=request.user).first()
    if AppliedJobs.objects.filter(user=request.user).filter(job=job).exists():
        apply_btn=1
    if SavedJobs.objects.filter(user=request.user).filter(job=job).exists():
        save_btn=1
    
    relevant_jobs=[]
    jobs1=Job.objects.filter(
		company__icontains=job.company).order_by('-date_posted')
    jobs2=Job.objects.filter(job_type_icontains=job.job_type).order_by('-date_posted')
    jobs3=Job.objects.filter(title__icontains=job.title).order_by('-date_posted')
    
    for i in jobs1:
        if len(relevant_jobs)>5:
            break;
        if i not in relevant_jobs and i!=job:
                relevant_jobs.append(i)
    
    for i in jobs2:
        if len(relevant_jobs)>5:
            break;
        if i not in relevant_jobs and i != job:
            relevant_jobs.append(i)
            
    for i in jobs3:
        if len(relevant_jobs) >5:
            break;
        if i not in relevant_jobs and i != job:
            relevant_jobs.append(i)
            
    return render(request, 'candidates/job_detail.html',{'job':job , 'profile':profile,'apply_button': apply_btn, 'save_button': save_btn, 'relevant_jobs': relevant_jobs, 'candidate_navbar': 1})
    
	
 
def saved_jobs(request):
	jobs=SavedJobs.objects.filter(
		user=request.user
	).order_by('-date_posted')
	
	return render(request, 'candidates/saved_jobs.html',{'jobs':jobs,'candidate_navbar': 1})

def applied_jobs(request):
    jobs=AppliedJobs.objects.filter(user=request.user).order_by('-date_posted')
    statuses=[]
    for job in jobs:
        if Selected.objects.filter(job=job.job).filter(applicant=request.user).exists():
            statuses.append(0)
        elif Applicants.objects.filter(job=job.job).filter(applicant=request.user).exists():
            statuses.append(1)
        else:
            statuses.append(2)
    zipped=zip(jobs,statuses)
    return render(request,'candidates/applied_jobs.html',{'zipped':zipped,'candidate_navbar':1})

@login_required
def intelligent_search(request):
    relevant_jobs=[]
    common=[]
    job_skills=[]
    user=request.user
    profile=Profile.objects.filter(user=user).first()
    my_skill_query=Skill.objects.filter(user=user)
    my_skills=[]
    for i in my_skill_query:
        my_skills.append(i.skill.lower())
    if profile:
        jobs=Job.objects.filter(
			job_type=profile.looking_for
		).order_by('-date_posted')
    else:
        jobs=Job.objects.all()
    for job in jobs:
        skills=[]
        sk=str(job.skills_req).split(",")
        for i in sk:
            skills.append(i.strip().lower())
        
        common_skills=list(set(my_skills) & set(skills))
    
        

@login_required
def my_profile(request):
    you=request.user
    profile=Profile.objects.filter(user=you).first()
    user_skills=Skill.objects.filter(user=you)
    if request.method == "POST":
        form=NewSkillForm(request.POST)
        if form.is_valid():
            data=form.save(commit=False)
            data.user=you
            data.save()
            return redirect('my-profile')
    else:
        form= NewSkillForm()
    context={
		'u':you,
		'profile': profile,
        'skills': user_skills,
        'form': form,
        'profile_page': "active",
	}
    return render(request,'candidates/profile.html',context)



@login_required
def edit_profile(request):
    you=request.user
    profile=Profile.objects.filter(user=you).first()
    if request.method=="POST":
        form=ProfileUpdateForm(request.POST,request.Files,instance=profile)
        if form.is_valid():
            data=form.save(commit=False)
            data.user=you
            data.save()
            return redirect('my-profile')
    else:
        form=ProfileUpdateForm(instance=profile)