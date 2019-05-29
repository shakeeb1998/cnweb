"""cnWeb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
import mysql.connector
import mysql.connector.pooling



mysqlPool = mysql.connector.pooling.MySQLConnectionPool(pool_name="pynative_pool",
                                                                  pool_size=15,
  host="ls-e720cd2221801d97ffe44f25c0713146ac0b3f85.czinalk9dhim.us-east-1.rds.amazonaws.com",
  user="qwerty",
  passwd="qwertyui",
database='dbqwerty'

)
a=mysqlPool.get_connection()

print('done connecting')
print(a.get_server_info())

urlpatterns = [
    path('admin/', admin.site.urls),

    path('cn/', include('cn.urls')),

]
