# Generated by Django 5.0.1 on 2024-02-27 19:15

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0004_tag_order_customer_order_product_product_tags"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="category",
            field=models.CharField(
                choices=[
                    ("Indoor", "Indoor"),
                    ("Outdoor", "Outdoor"),
                    ("Electronics", "Electronics"),
                    ("Toys", "Toys"),
                    ("Stationary", "Stationary"),
                ],
                max_length=100,
                null=True,
            ),
        ),
    ]
