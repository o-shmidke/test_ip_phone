import subprocess
import psutil
import os

from subprocess import check_output
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from psutil import NoSuchProcess
from service.forms import PermissionForm


class Service(object):
    name = 'apache2'
    pid = [0]

    def __init__(self):
        self.proc = self.get_proc()
        self.status = self.get_status()

    def get_proc(self):
        """Проверяет запущен ли процесс"""
        try:
            self.pid = check_output(["pidof", self.name]).split()
        except subprocess.CalledProcessError:
            pass
        try:
            self.proc = psutil.Process(int(self.pid[0]))
        except NoSuchProcess:
            self.proc = None
        return self.proc

    def get_name(self):
        """Получает имя  процесса"""
        return self.name

    def get_status(self):
        """Получает статус процесса"""
        if self.proc:
            self.status = self.proc.status()
        else:
            self.status = 'stop'
        return self.status


def get_data(request):
    """Получает данные из документа и о сервере, и отображает шаблон"""
    form = PermissionForm()
    with open('permission.txt', 'r') as perm:
        permission = perm.readline().strip()
    service = Service()
    name, status = service.get_name(), service.get_status()
    return render(request, 'base.html', {'form': form, 'name': name, 'status': status, 'perm': permission})


def control_service(request):
    """Управляет сервисом. Запускает, останавливает и перезапускает"""
    if request.method == 'POST':
        form = PermissionForm(request.POST)
        if form.is_valid():
            btn = form.data['btn']
            service = Service()
            name_service = service.get_name()
            if btn == 'start':
                os.system('sudo systemctl start %s' % name_service)
                print('start')
            if btn == 'stop':
                os.system('sudo systemctl stop %s' % name_service)
                print('stop')
            if btn == 'reboot':
                os.system('sudo systemctl restart %s' % name_service)
                print('reboot')

            with open('log_service.txt', 'w') as log_service:
                status = os.popen('sudo systemctl status %s' % name_service).read()
                for i in str(status):
                    log_service.writelines(i)
            return redirect('get_data')

        else:
            service = Service()
            name, status = service.name, service.status
            return render(request, 'base.html',
                          {'form': form, 'name': name, 'status': status, 'error': 'Недостаточно прав'})


@csrf_exempt
def save_permission(request):
    """Сохраняет состояние чекбокса в файл"""
    if request.method == 'POST':
        form = PermissionForm(request.POST)
        from django.utils.datastructures import MultiValueDictKeyError
        try:
            a = form.data['perm']
            checkbox = 'True'
        except MultiValueDictKeyError:
            checkbox = 'False'
        with open('permission.txt', 'w') as perm:
            perm.write(checkbox)
            return redirect('get_data')
