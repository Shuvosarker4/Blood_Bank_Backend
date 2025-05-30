from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

class BloodRequest(models.Model):
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('fulfilled', 'Fulfilled'),
        ('cancelled', 'Cancelled'),
    ]
    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('O+', 'O+'), ('O-', 'O-'),
    ]

    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_requests')
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES)
    units_required = models.PositiveIntegerField(default=1) 
    units_committed = models.PositiveIntegerField(default=0)  
    location = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    created_at = models.DateTimeField(auto_now_add=True)
    needed_by = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Request by {self.creator.email} for {self.blood_group}"

    def update_status(self):
        if self.units_required <= 0:
            self.status = 'fulfilled'
        elif self.status == 'fulfilled' and self.units_required > 0:
            self.status = 'open'
        self.save()

    @property
    def remaining_units(self):
        return max(self.units_required, 0)


class DonationAcceptance(models.Model):
    request = models.ForeignKey(BloodRequest, on_delete=models.CASCADE, related_name='acceptances')
    donor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='donations_accepted')
    accepted_at = models.DateTimeField(auto_now_add=True)
    units_committed = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('request', 'donor')

    def save(self, *args, **kwargs):
        if self.pk is None: 
            if self.request.status != 'open':
                raise ValidationError("This blood request is not open.")
            if self.units_committed > self.request.units_required:
                raise ValidationError("Donated units exceed remaining units needed.")

            super().save(*args, **kwargs)

            request = self.request
            request.units_committed += self.units_committed
            request.units_required -= self.units_committed
            request.units_required = max(request.units_required, 0)
            request.update_status()
        else:
            raise ValidationError("Editing donation is not allowed.")
