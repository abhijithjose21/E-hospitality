from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name='home'),
    path('ajax/check_username1/', views.check_username1, name='check_username1'),
    path('register', views.PatientRegistration, name='register'),
    path('ajax/check_username/', views.check_username, name='check_username'),
    path('login', views.Login, name='login'),
    path('logout',views.Logout, name='logout'),
    path('patient', views.PatientHome, name='patient'),
    path('admin1', views.AdminHome, name='admin1'),
    path('doctor', views.DoctorHome, name='doctor'),
    path('doctoradd', views.DoctorAdd, name='doctoradd'),
    path('doctorlist', views.listDoctors, name='doctorlist'),
    path('appointments_list/', views.appointment_list, name='appointment_list'),
    path('appointments', views.appointment_create, name='appointment_create'),
    path('appointments/<int:appointment_id>/', views.appointment_detail, name='appointment_detail'),
    path('appointments/<int:appointment_id>/delete/', views.appointment_delete, name='appointment_delete'),
    path('doc_appointmentlist', views.doc_appointmentlist, name='doc_appointmentlist'),
    path('doc_appointments/<int:appointment_id>/', views.doc_appointmentdetail, name='doc_appointmentdetail'),
    path('admin_appointmentlist', views.admin_appointmentlist, name='admin_appointmentlist'),
    path('admin_appointments/<int:appointment_id>/', views.admin_appointmentdetail, name='admin_appointments'),
    path('prescriptions',views.create_prescription, name='create_prescription'),
    path('prescriptionlist',views.prescription_list,name='prescriptionlist'),
    path('doc_patientlist',views.doc_patientlist,name='doc_patientlist'),
    path('doc_patientdetail/<int:patient_id>',views.doc_patientdetail,name='doc_patientdetail'),
    path('billing/new/', views.create_billing, name='create_billing'),
    path('billing/', views.pat_billing_list, name='billing_list'),
    path('create-checkout-session',views.create_checkout_session,name='create-checkout-session'),
    path('success/',views.success,name='success'),
    path('cancel/',views.cancel,name='cancel'),
    path('billing_list',views.billing_list,name='billing_list'),
    path('medicine',views.medicinecreate,name='medicine')

]