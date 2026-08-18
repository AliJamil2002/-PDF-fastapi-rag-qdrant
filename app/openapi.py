from fastapi.openapi.utils import get_openapi


def custom_openapi(app):
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )

    # Find the upload request schema
    upload_schema = openapi_schema["paths"]["/upload"]["post"]["requestBody"][
        "content"
    ]["multipart/form-data"]["schema"]

    body_schema = openapi_schema["components"]["schemas"][
        "Body_upload_files_upload_post"
    ]

    # Tell OpenAPI that files are binary files
    body_schema["properties"]["files"]["items"] = {
        "type": "string",
        "format": "binary",
    }

    app.openapi_schema = openapi_schema

    return app.openapi_schema