from django.db import models


# Create your models here.

class PatientReg(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    user_name = models.CharField(max_length=100,unique=True)
    password = models.CharField(max_length=100)
    con_password = models.CharField(max_length=100)


class LoginType(models.Model):
    user_name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    type = models.CharField(max_length=100)


class DoctorReg(models.Model):
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    user_name = models.CharField(max_length=100,unique=True)
    password = models.CharField(max_length=100)
    con_password = models.CharField(max_length=100)


class Appointments(models.Model):

    patient = models.ForeignKey(PatientReg, on_delete=models.CASCADE)
    doctor = models.ForeignKey(DoctorReg, on_delete=models.CASCADE)
    appointment_date = models.DateTimeField()
    reason = models.TextField()



class Medication(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()


class Prescription(models.Model):
    doctor = models.ForeignKey(DoctorReg, on_delete=models.CASCADE, related_name='prescriptions')
    patient = models.ForeignKey(PatientReg, on_delete=models.CASCADE, related_name='patient_prescriptions')
    medication = models.ForeignKey(Medication, on_delete=models.CASCADE)
    dosage = models.CharField(max_length=100)
    frequency = models.CharField(max_length=100)
    date_prescribed = models.DateTimeField(auto_now_add=True)



class Billing(models.Model):
    patient = models.ForeignKey(PatientReg, on_delete=models.CASCADE, related_name='bills')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    date_issued = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)