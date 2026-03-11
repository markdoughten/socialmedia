# linkedin.py
import base64
import requests

REGISTER_UPLOAD = "https://api.linkedin.com/v2/assets?action=registerUpload"
UGC_POSTS = "https://api.linkedin.com/v2/ugcPosts"

def _get_person_urn(access_token):
    headers = {"Authorization": f"Bearer {access_token.strip()}"}
    r = requests.get("https://api.linkedin.com/v2/userinfo", headers=headers)
    r.raise_for_status()
    data = r.json()
    return f"urn:li:person:{data['sub']}"

def _register_upload(access_token, person_urn):
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "X-Restli-Protocol-Version": "2.0.0",
        "Content-Type": "application/json",
    }

    payload = {
        "registerUploadRequest": {
            "recipes": ["urn:li:digitalmediaRecipe:feedshare-image"],
            "owner": person_urn,
            "serviceRelationships": [
                {
                    "relationshipType": "OWNER",
                    "identifier": "urn:li:userGeneratedContent",
                }
            ],
        }
    }

    r = requests.post(REGISTER_UPLOAD, headers=headers, json=payload)
    r.raise_for_status()

    data = r.json()["value"]

    asset = data["asset"]
    upload_url = data["uploadMechanism"][
        "com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest"
    ]["uploadUrl"]

    return asset, upload_url

def _upload_image(upload_url, access_token, image_bytes):
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/octet-stream",
    }

    r = requests.post(upload_url, headers=headers, data=image_bytes)
    r.raise_for_status()

def _create_post(access_token, person_urn, text, asset):
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "X-Restli-Protocol-Version": "2.0.0",
        "Content-Type": "application/json",
    }

    payload = {
        "author": person_urn,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {"text": text},
                "shareMediaCategory": "IMAGE",
                "media": [
                    {
                        "status": "READY",
                        "media": asset,
                        "title": {"text": "Generated Image"},
                    }
                ],
            }
        },
        "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"},
    }

    r = requests.post(UGC_POSTS, headers=headers, json=payload)
    r.raise_for_status()

    return r.json()

def send_to_linkedin(linkedin_api_key, text, image):
    """
    linkedin_api_key : LinkedIn OAuth access token
    text             : Post text
    image            : base64 encoded image string
    """

    access_token = linkedin_api_key
    person_urn = _get_person_urn(access_token)
    asset, upload_url = _register_upload(access_token, person_urn)
    _upload_image(upload_url, access_token, image)
    response = _create_post(access_token, person_urn, text, asset)

    return response