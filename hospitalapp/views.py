from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from .models import PatientReg, LoginType, DoctorReg, Appointments, Prescription, Medication, Billing
from django.contrib import messages
from django.contrib.auth import logout as auth_logout, authenticate
from django.contrib.auth import authenticate, login as auth_login
import stripe


# Create your views here.
#
# def PatientRegistraion(request):
#     Patient_Reg = PatientReg()
#     Login_Type = LoginType()
#
#     if request.method == 'POST':
#         Patient_Reg.first_name = request.POST['first_name']
#         Patient_Reg.last_name = request.POST['last_name']
#         Patient_Reg.date_of_birth = request.POST['date_of_birth']
#         Patient_Reg.phone_number = request.POST['phone_number']
#         Patient_Reg.address = request.POST['address']
#         Patient_Reg.user_name = request.POST['user_name']
#         Patient_Reg.password = request.POST['password']
#         Patient_Reg.con_password = request.POST['con_password']
#
#         Login_Type.user_name = request.POST['user_name']
#         Login_Type.password = request.POST['password']
#         Login_Type.type = 'patient'
#
#         if request.POST['password'] == request.POST['con_password']:
#
#             Patient_Reg.save()
#             Login_Type.save()
#             messages.info(request, 'Registration Successfull')
#             return redirect('login')
#         else:
#             messages.info(request, 'Registration Not Successfull')
#             return redirect('register')
#
#     return render(request, 'register.html')
#
def check_username1(request):
    username = request.GET.get('username', None)
    data = {
        'is_taken': PatientReg.objects.filter(user_name=username).exists()
    }
    return JsonResponse(data)

def PatientRegistration(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        date_of_birth = request.POST['date_of_birth']
        phone_number = request.POST['phone_number']
        address = request.POST['address']
        user_name = request.POST['user_name']
        password = request.POST['password']
        con_password = request.POST['con_password']

        if password != con_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('register')

        if PatientReg.objects.filter(user_name=user_name).exists():
            messages.error(request, 'Username already exists.')
            return redirect('register')

        patient_reg = PatientReg(
            first_name=first_name,
            last_name=last_name,
            date_of_birth=date_of_birth,
            phone_number=phone_number,
            address=address,
            user_name=user_name,
            password=password,
            con_password=con_password
        )
        login_type = LoginType(
            user_name=user_name,
            password=password,
            type='patient'
        )

        patient_reg.save()
        login_type.save()
        messages.success(request, 'Registration successful.')
        return redirect('login')

    return render(request, 'register.html')
# def Login(request):
#     if request.method == 'POST':
#         user_name = request.POST['user_name']
#         password = request.POST['password']
#         user = LoginType.objects.filter(user_name=user_name, password=password, type='patient')
#
#         try:
#             if user is not None:
#                 user_details = LoginType.objects.get(user_name=user_name, password=password)
#                 user_name = user_details.user_name
#                 type = user_details.type
#
#                 # request.session['user_name'] = user_name
#                 # request.session['user_type'] = type
#
#                 if type == 'patient':
#                     request.session['user_name'] = user_name
#                     return redirect('patient')
#                 elif type == 'admin':
#                     request.session['user_name'] = user_name
#                     return redirect('admin1')
#                 elif type == 'doctor':
#                     request.session['user_name'] = user_name
#                     return redirect('doctor')
#             else:
#                 messages.error(request, "Invalid Username or password")
#
#         except:
#             messages.error(request, 'invalid role')
#
#     return render(request, 'login.html')

def Login(request):
    if request.method == 'POST':
        user_name = request.POST['user_name']
        password = request.POST['password']
        user = LoginType.objects.filter(user_name=user_name, password=password).first()

        if user is not None:
            user_name = user.user_name
            type = user.type

            request.session['user_name'] = user_name

            if type == 'patient':
                return redirect('patient')
            elif type == 'admin':
                return redirect('admin1')
            elif type == 'doctor':
                return redirect('doctor')
        else:
            # Check if the user is a superuser
            user = authenticate(request, username=user_name, password=password)
            if user is not None and user.is_superuser:
                auth_login(request, user)
                request.session['user_name'] = user.username
                return redirect('admin1')
            else:
                messages.error(request, "Invalid Username or Password")

    return render(request, 'login.html')
def Logout(request):
    auth_logout(request)
    return redirect('login')


def PatientHome(request):
    return render(request, 'patient/pat_index.html')


def AdminHome(request):
    return render(request, 'admin/index.html')


def DoctorHome(request):
    return render(request, 'doctor/index.html')


def home(request):
    return render(request, 'index.html')

#
# def DoctorAdd(request):
#     Doctor_Reg = DoctorReg()
#     Login_Type = LoginType()
#
#     if request.method == 'POST':
#         Doctor_Reg.name = request.POST['name']
#         Doctor_Reg.department = request.POST['department']
#         Doctor_Reg.user_name = request.POST['user_name']
#         Doctor_Reg.password = request.POST['password']
#         Doctor_Reg.con_password = request.POST['con_password']
#
#         Login_Type.user_name = request.POST['user_name']
#         Login_Type.password = request.POST['password']
#         Login_Type.type = 'doctor'
#         user_name = request.POST['user_name']
#
#         if request.POST['password'] != request.POST['con_password']:
#             messages.info(request, 'Registration Not Successfull')
#             return redirect('doctoradd')
#
#         elif Doctor_Reg.objects.filter(user_name=user_name).exists():
#             messages.error(request, 'Username already exists.')
#
#         else:
#             Doctor_Reg.save()
#             Login_Type.save()
#             messages.info(request, 'Registration Successfull')
#             return redirect('admin1')
#
#
#     return render(request, 'admin/doctoradd.html',{'message':messages})
def check_username(request):
    username = request.GET.get('username', None)
    data = {
        'is_taken': DoctorReg.objects.filter(user_name=username).exists()
    }
    return JsonResponse(data)

def DoctorAdd(request):
    if request.method == 'POST':
        name = request.POST['name']
        department = request.POST['department']
        user_name = request.POST['user_name']
        password = request.POST['password']
        con_password = request.POST['con_password']

        if password != con_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('doctoradd')

        elif DoctorReg.objects.filter(user_name=user_name).exists():
            messages.error(request, 'Username already exists.')

        else:
            doctor = DoctorReg(name=name, department=department, user_name=user_name, password=password, con_password=con_password)
            login_type = LoginType(user_name=user_name, password=password, type='doctor')
            doctor.save()
            login_type.save()
            messages.success(request, 'Registration successful.')
            return redirect('admin1')

    return render(request, 'admin/doctoradd.html')
def listDoctors(request):
    doctors = DoctorReg.objects.all()

    return render(request, 'doctorlist.html', {'doctors': doctors})



def appointment_list(request):
    patient = PatientReg.objects.get(user_name=request.session.get('user_name'))
    appointments = Appointments.objects.filter(patient__id=patient.id)
    return render(request, 'patient/appointment_list.html', {'appointments': appointments})



def appointment_create(request):

    if request.method == 'POST':
        doctor_id = request.POST.get('doctor')
        appointment_date = request.POST.get('appointment_date')
        reason = request.POST.get('reason')
        doctor = get_object_or_404(DoctorReg, id=doctor_id)
        patient = PatientReg.objects.get(user_name=request.session.get('user_name'))
        Appointments.objects.create(patient=patient, doctor=doctor, appointment_date=appointment_date, reason=reason)
        return redirect('patient')
    else:
        doctors = DoctorReg.objects.all()
        patient = PatientReg.objects.get(user_name=request.session.get('user_name'))
        return render(request, 'patient/appointment_form.html', {'doctors': doctors,'patient':patient})



def appointment_detail(request, appointment_id):
    appointment = get_object_or_404(Appointments, id=appointment_id)
    return render(request, 'patient/appointment_detail.html', {'appointment': appointment})



def appointment_delete(request, appointment_id):
    appointment = get_object_or_404(Appointments, id=appointment_id)
    if request.method == 'POST':
        appointment.delete()
        return redirect('appointment_list')
    return render(request, 'appointments/appointment_confirm_delete.html', {'appointment': appointment})


def doc_appointmentlist(request):
    doctor = DoctorReg.objects.get(user_name=request.session.get('user_name'))
    appointments = Appointments.objects.filter(doctor__id=doctor.id)
    return render(request, 'doctor/doc_appointmentlist.html', {'appointments': appointments})


def doc_appointmentdetail(request, appointment_id):
    appointment = get_object_or_404(Appointments, id=appointment_id)
    return render(request, 'doctor/doc_appointmentdetail.html', {'appointment': appointment})


def admin_appointmentlist(request):
    appointments = Appointments.objects.all()
    return render(request, 'admin/admin_appointmentlist.html', {'appointments': appointments})


def admin_appointmentdetail(request, appointment_id):
    appointment = get_object_or_404(Appointments, id=appointment_id)
    return render(request, 'admin/admin_appointmentdetail.html', {'appointment': appointment})


def create_prescription(request):
    if request.method == 'POST':
        patient_id = request.POST.get('patient')
        medication_id = request.POST.get('medication')
        dosage = request.POST.get('dosage')
        frequency = request.POST.get('frequency')

        patient = PatientReg.objects.get(id=patient_id)
        medication = Medication.objects.get(id=medication_id)
        doctor = DoctorReg.objects.get(user_name=request.session.get('user_name'))

        Prescription.objects.create(
            doctor=doctor,
            patient=patient,
            medication=medication,
            dosage=dosage,
            frequency=frequency
        )
        return redirect('doctor')

    patients = PatientReg.objects.all()
    medications = Medication.objects.all()
    return render(request, 'doctor/create_prescription.html', {'patients': patients, 'medications': medications})


def prescription_list(request):
    patient = PatientReg.objects.get(user_name=request.session.get('user_name'))
    prescription = Prescription.objects.filter(patient__id=patient.id)
    return render(request, 'patient/prescription_list.html', {'prescription': prescription})


def doc_patientlist(request):
    doctor = DoctorReg.objects.get(user_name=request.session.get('user_name'))
    patient_ids = Appointments.objects.filter(doctor=doctor).values_list('patient', flat=True).distinct()
    patients = PatientReg.objects.filter(id__in=patient_ids)

    return render(request, 'doctor/patientlist.html', {'patients': patients})
def doc_patientdetail(request, patient_id):
    prescription = Prescription.objects.filter(patient__id=patient_id)
    appointment = Appointments.objects.filter(patient__id=patient_id)
    data={
        'prescription': prescription,
        'appointment' : appointment
    }
    return render(request, 'doctor/doc_patientdetail.html', {'data':data})




def create_billing(request):
    if request.method == 'POST':
        patient_id = request.POST.get('patient')
        amount = request.POST.get('amount')
        description = request.POST.get('description')
        date_issued = request.POST.get('date_issued')


        if patient_id and amount and description and date_issued:
            patient = PatientReg.objects.get(id=patient_id)
            Billing.objects.create(
                patient=patient,
                amount=amount,
                description=description,
                date_issued=date_issued
            )
            return redirect('admin1')

    patients = PatientReg.objects.all()
    return render(request, 'admin/billing.html', {'patients': patients})

def pat_billing_list(request):
    patient = PatientReg.objects.get(user_name=request.session.get('user_name'))
    bills = Billing.objects.filter(patient__id=patient.id)
    return render(request, 'patient/pat_billinglist.html', {'bills': bills})





def create_checkout_session(request):

    patient = PatientReg.objects.get(user_name=request.session.get('user_name'))

    bills = Billing.objects.filter(patient__id=patient.id, is_paid=False)

    if request.method == 'POST' and bills.exists():
        stripe.api_key = settings.STRIPE_SECRET_KEY

        line_items = []
        for bill in bills:
            line_item = {
                'price_data': {
                    'currency': 'INR',
                    'unit_amount': int(bill.amount * 100),
                    'product_data': {
                        'name': bill.description,
                    },
                },
                'quantity': 1,
            }
            line_items.append(line_item)

        if line_items:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=line_items,
                mode='payment',
                success_url=request.build_absolute_uri(reverse('success')),
                cancel_url=request.build_absolute_uri(reverse('cancel')),
            )

            return redirect(checkout_session.url, code=303)


    return render(request, 'billing_list.html', {'bills': bills})


def success(request):
    patient = PatientReg.objects.get(user_name=request.session.get('user_name'))
    bills = Billing.objects.filter(patient__id=patient.id)

    for bills in bills:
        bills.is_paid=True
        bills.save()
    return render(request,'patient/success.html')

def cancel(request):
    return render(request,'patient/cancel.html')

def billing_list(request):

    bills = Billing.objects.all()
    return render(request, 'admin/billinglist.html', {'bills': bills})

def medicinecreate(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')

        Medication.objects.create(
            name=name,
            description=description
        )

        return redirect('medicine')
    else:
        medicine = Medication.objects.all()
    return render(request,'doctor/medicine.html',{'medicine' : medicine})