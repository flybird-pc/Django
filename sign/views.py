from django.shortcuts import render, get_object_or_404

from django.http import HttpResponse,HttpResponseRedirect

from django.views.decorators.csrf import csrf_exempt

from django.contrib import auth

from django.contrib.auth.decorators import login_required

from sign.models import Event,Guest

#from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger

# Create your views here.

# def guest_search_name(request):
#     username = request.session.get('user', '')
#     guest_search_name = request.GET.get("real_name", "")
#     guest_list = Guest.objects.filter(realname__contains=guest_search_name)
#
#     paginator = Paginator(guest_list, 2)  # 创建每页2条数据的分页器
#     page = request.GET.get('page')  # 通过get请求得到当前要显示的第几页数据
#     try:
#         contacts = paginator.page(page)  # 获取第page页的数据，如果没有抛出异常
#     except PageNotAnInteger:
#         # 如果page页不是整数，取第1页数据
#         contacts = paginator.page(1)
#     except EmptyPage:
#         # 如果page不在范围，取最后1页数据
#         contacts = paginator.page(paginator.num_pages)
#     return render(request, "guest_manage.html", {"user": username, "guests": contacts})


def index(request):
    return render(request, "index.html")

#登录动作
def login_action(request):
    if request.method == "POST":
        username = request.POST.get("username","")
        password = request.POST.get("password","")
        # if username == 'test' and password == '123456':
        #     #return render(request,"login_success.html")
        #     response = HttpResponseRedirect("/login_success/")
        #     #response.set_cookie("user",username,3600) #添加浏览器cookie:user表示写入浏览器的Cookie名;username由用户在登录页面上输入的用户名,3600用于设置Cookie信息在浏览器中保持的时间，默认单位为秒
        #     request.session["user"] = username #将session记录到浏览器
        #     return response
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            request.session["user"] = username
            response = HttpResponseRedirect("/login_success/")
            return response

        else:
            return render(request,"index.html",{"error":"用户名或密码错误"})

#登录成功页
@login_required
def login_success(request):
    #username = request.COOKIES.get("user","")#读取浏览器cookie
    event_list = Event.objects.all()  # 查询所有发布会对象（数据）
    username = request.session.get("user", "")  # 读取浏览器session
    return render(request,"login_success.html",{"user":username,"events":event_list})

#发布会名称搜搜
@login_required
def search_name(request):
    username = request.session.get('user', '')
    search_name = request.GET.get("name", "")
    event_list = Event.objects.filter(name__contains=search_name)
    return render(request, "login_success.html", {"user": username, "events": event_list})

@login_required
def guest_manage(request):
    guest_list = Guest.objects.all() # 查询所有嘉宾对象（数据）
    username = request.session.get("user", "")  # 读取浏览器session
    return render(request, "guest_manage.html", {"user": username, "guests": guest_list})

#嘉宾搜搜
@login_required
def search_name(request):
    username = request.session.get('user', '')
    search_name = request.GET.get("real_name", "")
    guest_list = Guest.objects.filter(real_name__contains=search_name)
    return render(request, "guest_manage.html", {"user": username, "guests": guest_list})


# 签到页面
@login_required
def sign_index(request, eid):
    event = get_object_or_404(Event, id=eid)
    return render(request, "sign_index.html", {"event": event})


# 签到动作
@login_required
def sign_index_action(request, eid):
    event = get_object_or_404(Event, id=eid)
    phone = request.POST.get("phone", "")
    print(phone)
    result = Guest.objects.filter(phone=phone)
    if not result:
        return render(request, "sign_index.html", {"event": event, "hint": "手机号错误！"})
    result = Guest.objects.filter(phone=phone, event_id=eid)
    if not result:
        return render(request, "sign_index.html", {"event": event, "hint": "发布会id或者手机号错误！"})
    result = Guest.objects.get(phone=phone, event_id=eid)
    if result.sign:
        return render(request, "sign_index.html", {"event": event, "hint": "用户已签到！"})
    else:
        Guest.objects.filter(phone=phone, event_id=eid).update(sign="1")
        return render(request, "sign_index.html", {"event": event, "hint": "签到成功！", "guest": result})


#退出系统
@login_required
def logout(request):
    auth.logout(request)    #退出登录
    response = HttpResponseRedirect("/index/")
    return response


def home(request):
    return render(request, "home.html")

# 404页面
@csrf_exempt
def page_not_found(request, exception):
    return render(request, "404.html")

# 500页面
def page_error(request):
    return render(request, '500.html')