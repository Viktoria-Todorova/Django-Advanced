from time import time

from django.conf import settings
from django.http import HttpResponseForbidden
from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin
from django.utils.timezone import now


class RequestLoginMiddleware(MiddlewareMixin):
    def process_request(self, request):
        self.start_time=time()

    def process_response(self, request, response):
        print(f"{request.method} {request.path} - {now()}; Executed in {time() - self.start_time}")
        return response

class TrainingVesionMiddleware(MiddlewareMixin):
    def process_response(self, request,response):
        response['X-Training-Version'] = '1.0'
        return response
#when we rerun we have 2 request admin-login and devtools.json and it will count 2,4,etc
class TotalRequestsCounter(MiddlewareMixin):
    total_requests=0
    def process_request(self, request):
       TotalRequestsCounter.total_requests+=1
       request._total_requests=TotalRequestsCounter.total_requests


    def process_response(self, request,response):
        response['X-Total-Requests'] = TotalRequestsCounter.total_requests
        return response

class IPWhitelistMiddleware(MiddlewareMixin):
    def process_request(self, request):
        client_ip = request.META.get('REMOTE_ADDR','')
        allowed_ips = getattr(settings,'ALLOWED_IPS',[])
        if client_ip not in allowed_ips:
            return HttpResponseForbidden('Access Denied for this IP address')

class SessionRateLimitingMiddleware(MiddlewareMixin):
    session_key = 'rate_limit_messages'
    window_seconds=60
    def process_request(self, request):
        allowed_requests=getattr(settings,'REQUESTS_PER_MINUTE',10)
        now = timezone.now().timestamp()
        window_start = now - self.window_seconds
        recent_timestamps = [
            t
            for t in request.session.get(self.session_key, [])
            if t > window_start
        ]

        if len(recent_timestamps) >= allowed_requests:
            return HttpResponseForbidden('Too many requests')

        recent_timestamps.append(now)
        request.session[self.session_key] = recent_timestamps

class SuspiciousActivityMiddleware(MiddlewareMixin):
    blocked_params = {'is_admin'}
    def process_request(self, request):
        findings=[]
        findings.extend(self._scan_queryset(request.GET))
        findings.extend(self._scan_queryset(request.POST))
        if findings:
            return HttpResponseForbidden('Suspicious activity detected')

    def _scan_queryset(self, querydict):
        findings = []
        for key, value in querydict.lists():
            if key in self.blocked_params:
                findings.append(key)

        return findings
