from django.shortcuts import render
from django.db.models import Q
from django.views.generic import ListView
from directory.models import Teacher,Subjects
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from .forms import AddTeacherForm
from django.http import HttpResponse,JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
import io,csv

# Create your views here.

class LoginView(View):
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            error = "Invalid credentials"
            return render(request, "login.html", {'error': error})

def logout_view(request):
    logout(request)
    return redirect('login')

"""View for Listing and Filtering Teachers based
on the First Letter of their Last Name or subjects.
"""
class TeachersListView(ListView):
    model = Teacher
    context_object_name = 'teachers_list'
    template_name = 'teachers_list.html'

    def get_queryset(self):
        filter_val = self.request.GET.get('filter', '')
        new_context = Teacher.objects.filter(
            Q(last_name__istartswith=filter_val) | Q(subjects__name__contains=filter_val)
        ).distinct()
        return new_context

    def get_context_data(self, **kwargs):
        context = super(TeachersListView, self).get_context_data(**kwargs)
        context['filter'] = self.request.GET.get('filter', '')
        context['subjects'] = Subjects.objects.all()
        return context


"""Bulk Upload data to Teachers from csv File.
Check constraints - Unique Email Id and Max Subjects to be 5
"""
class TeachersBulkUpload(View):
    @method_decorator(login_required)
    def post(self, request):
        paramFile = io.TextIOWrapper(request.FILES['data_file'].file)
        portfolio1 = csv.DictReader(paramFile)
        list_of_dict = list(portfolio1)
        subject_ids = []
        error_list = []
        success_msg = []
        try:
            for row in list_of_dict:
                if row['Email Address']:
                # if any(x.strip() for x in row):
                    subject_ids.clear()
                    new_email = row['Email Address']
                    email_exists = Teacher.check_email_exists(self,new_email)
                    subjects = list(row['Subjects taught'].split(","))
                    subjects_count = len(subjects)
                    if subjects_count > 5  or email_exists:
                        error_list = [{"message": "Some entries couldnt be added , please Check for duplicate email Id and verify if Number of Subjects is less than 5"}]
                        continue
                    else:
                        for subject in subjects:
                            subject_id = Subjects.search_for_sub(self,name=subject)
                            subject_ids.append(subject_id)
                        objs= Teacher(first_name=row['First Name'],last_name=row['Last Name'],phone_number=row['Phone Number'],email=row['Email Address'],room_number=row['Room Number'],profile_pic='uploads/'+ row['Profile picture'])
                        objs.save()
                        for i in subject_ids:
                            objs.subjects.add(i)
                    success_msg = {'success':'True'}
                else:
                    continue

        except Exception as e:
            error_list.append({"message": "Unexpected Error"})

        return render(request, 'bulk_upload.html', {
        'error_list': error_list,'success_msg':success_msg })

"""Add an entry in Teacher from form
"""
@login_required
def add_teacher(request):
    if request.method == 'POST':
        form = AddTeacherForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = AddTeacherForm()

    return render(request, 'add_teacher.html', {'form': form})

"""Detail View for A single Teacher
"""
class TeacherDetailView(View):
    def get(self, request, *args, **kwargs):
        teacher = get_object_or_404(Teacher, pk=kwargs['pk'])
        context = {'teacher': teacher}
        return render(request, 'teacher_detail.html', context)
