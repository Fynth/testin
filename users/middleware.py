from rest_framework.authtoken.models import Token

class TokenMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if 'Authorization' in request.headers:
            try:
                token_key = request.headers['Authorization'].split(' ')[1]
                token = Token.objects.get(key=token_key)
                request.user = token.user
            except Token.DoesNotExist:
                pass 

        response = self.get_response(request)
        return response