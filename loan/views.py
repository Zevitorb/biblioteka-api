from rest_framework.generics import CreateAPIView
from .models import Loan
from .serializer import LoanSerializer
from rest_framework.permissions import (
    IsAdminUser,
)
from django.utils import timezone
from rest_framework_simplejwt.authentication import JWTAuthentication
from copies.models import Copy
from users.models import User
from datetime import datetime, timedelta
from rest_framework.exceptions import ValidationError


class LoanView(CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

    queryset = Loan.objects.all()
    serializer_class = LoanSerializer

    def perform_create(self, serializer):
        copy_id = self.request.data.get("copy")
        copy = Copy.objects.get(id=copy_id)

        if copy.disponibilidade == False:
            raise ValidationError("A cópia não está disponível.")

        user_id = self.request.data.get("user")
        user = User.objects.get(id=user_id)


        copy.disponibilidade = False
        copy.save()


        prazo = self.calculate_prazo()
        serializer.save(user=user, copy=copy, prazo=prazo)

    def calculate_prazo(self):
        current_date = timezone.now()
        prazo = current_date + timedelta(days=7)

        if prazo.weekday() >= 5:
            prazo += timedelta(days=2)

        return prazo
