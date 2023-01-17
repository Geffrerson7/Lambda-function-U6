import mercadopago
import os
import json

def lambda_handler(event, context):
    sdk = mercadopago.SDK(os.environ["ACCESS_TOKEN"])
    bodyGet=json.loads(event["body"])
    try:
        payment_data = {
            "transaction_amount": float(bodyGet["transaction_amount"]),
            "token": bodyGet["token"],
            "installments": int(bodyGet["installments"]),
            "payment_method_id": bodyGet["payment_method_id"],
            "payer": {
                "email": bodyGet["payer"]["email"],
                "identification": {
                    "type": bodyGet["payer"]["identification"]["type"],
                    "number": bodyGet["payer"]["identification"]["number"],
                },
            },
        }

        payment_response = sdk.payment().create(payment_data)
        paymentR=payment_response["response"]
        status = {
            "status": paymentR["status"],
            "status_detail": paymentR["status_detail"],
            "id": paymentR["id"],
        }
        
        return {
            "statusCode": 201,
            "body": status,
        }
    except Exception as error:
        return {"statusCode": 500, "body": json.dumps(str(error))}