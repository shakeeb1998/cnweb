from django.http import JsonResponse
from pyfcm import FCMNotification
import uuid
import firebase_admin


from firebase_admin import credentials


name=str(uuid.uuid1())
cred = credentials.Certificate('pvt.json')
y=firebase_admin.initialize_app(credential=cred,name=name)

def notifier(request):
    print(request.GET.get('uid'))
    print("notifiuer")
    notify(string=request.GET.get('uid'),title="djskj",body='saknddnksankdas')
    return JsonResponse({'success': 'jjjj'})




def notify(string,title,body):
    registration_id =string


    message_title = title
    message_body = body
    api = "AAAAFQUjNgo:APA91bHc3Ehodau73WUboF2JtIJRV8sKOCnnXVsrDCxt_8OCM9erGNx72FQX59Hd5uuDpJWadUTCxtbHMMC4Zn9UyrIpBF0cCFbgPMr1R5v-Ak7GdmOOZxxPA7bimNoBaThkZAVlaIJZ"

    push_service = FCMNotification(api_key=api)
    print(string)
    # FCMNotification.notify_single_device(registration_id=registration_id,message_title=message_title,message_body=message_body,)
    result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title,  message_body=message_body)
    print('-----------------------------------------------------')
    print(result)
