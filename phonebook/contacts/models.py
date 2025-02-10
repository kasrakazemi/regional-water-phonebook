from django.db import models

class Contact(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    phone = models.CharField(max_length=20, null=False, blank=False)  # Ensure null=False

    def __str__(self):
        return self.name
