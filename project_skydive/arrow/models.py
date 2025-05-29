from django.db import models

# Create your models here.

class Landing(models.Model):
    latt = models.CharField(max_length=128)
    long = models.CharField(max_length=128)
    
    def __str__(self):
        return self.latt+'---'+self.long
    
class Drop(models.Model):
    latt = models.CharField(max_length=128)
    long = models.CharField(max_length=128)
    
    def __str__(self):
        return self.latt+'---'+self.long
 
class Skydive(models.Model):
    latt = models.CharField(max_length=128)
    long = models.CharField(max_length=128)
    
    def __str__(self):
        return self.latt+'---'+self.long
