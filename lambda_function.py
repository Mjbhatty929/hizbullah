import boto3
from PIL import Image
import io

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    
    # Get bucket and file details from the S3 event
    source_bucket = event['Records'][0]['s3']['bucket']['name']
    source_key = event['Records'][0]['s3']['object']['key']
    
    # Destination bucket
    destination_bucket = 'haji-lam2'
    destination_key = source_key.rsplit('.', 1)[0] + '.png'
    
    try:
        # Fetch the file from the source bucket
        response = s3.get_object(Bucket=source_bucket, Key=source_key)
        image_content = response['Body'].read()
        
        # Convert the image to PNG using Pillow
        image = Image.open(io.BytesIO(image_content))
        output_buffer = io.BytesIO()
        image.save(output_buffer, 'PNG')
        output_buffer.seek(0)
        
        # Upload the converted image to the destination bucket
        s3.put_object(
            Bucket=destination_bucket,
            Key=destination_key,
            Body=output_buffer,
            ContentType='image/png'
        )
        
        return {
            'statusCode': 200,
            'body': f"Image successfully converted and saved to {destination_bucket}/{destination_key}"
        }
    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': "Error processing image"
        }
