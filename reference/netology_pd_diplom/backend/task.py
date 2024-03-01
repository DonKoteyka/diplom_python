from celery import shared_task
from requests import get

from yaml import load as load_yaml, Loader

from backend.models import Shop, Category, Product, ProductInfo, Parameter, ProductParameter, User
from netology_pd_diplom.celery_app import app
from typing import Type

from django.conf import settings
from django.core.mail import EmailMultiAlternatives


from backend.models import ConfirmEmailToken, User

@shared_task
# @app.task(serializer='json')
def price_update(url, user_id):
    print("task start")
    stream = get(url).content
    data = load_yaml(stream, Loader=Loader)
    shop, _ = Shop.objects.get_or_create(name=data['shop'], user_id=user_id)
    for category in data['categories']:
        category_object, _ = Category.objects.get_or_create(id=category['id'], name=category['name'])
        category_object.shops.add(shop.id)
        category_object.save()
    ProductInfo.objects.filter(shop_id=shop.id).delete()
    for item in data['goods']:
        product, _ = Product.objects.get_or_create(name=item['name'], category_id=item['category'])

        product_info = ProductInfo.objects.create(product_id=product.id,
                                                  external_id=item['id'],
                                                  model=item['model'],
                                                  price=item['price'],
                                                  price_rrc=item['price_rrc'],
                                                  quantity=item['quantity'],
                                                  shop_id=shop.id)
        for name, value in item['parameters'].items():
            parameter_object, _ = Parameter.objects.get_or_create(name=name)
            ProductParameter.objects.create(product_info_id=product_info.id,
                                            parameter_id=parameter_object.id,
                                            value=value)
@shared_task
# @app.task()
def send_email_new_user(user_id):
    print("task start")
    user = User.objects.get(id=user_id)
    token, _ = ConfirmEmailToken.objects.get_or_create(user_id=user.pk)

    msg = EmailMultiAlternatives(
        # title:
        f"Password Reset Token for {user.email}",
        # message:
        token.key,
        # from:
        settings.EMAIL_HOST_USER,
        # to:
        [user.email]
    )
    msg.send()
    return f'Отправленно! token:{token.key}'



