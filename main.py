# from fastapi import FastAPI, Response, HTTPException, Depends, Request, requests
#
# import json
# import uvicorn
# from collections import OrderedDict
# import base64
# import re
#
#
#
# app = FastAPI()
#
# # etl = pipeline.ETL(config_file="pipeline/config/config.json",
# #                    key_file="pipeline/credentials/deployer-service-account-key-file.json"
# #                    )
#
#
# @app.get('/some_endpoint')
# async def pub_sub_message(app: str,som_var :str, filter: str):
#     """Endpoint receive message from pubsub and
#      starts workflow"""
#
#
#
#
#
#     out = OrderedDict()
#     out["status"] = "success"
#     out["message"] = "Workflow execution started"
#
#     return Response(
#         content=json.dumps(out, indent=1),
#         status_code=200,
#         media_type="application/json"
#     )





if __name__ == "__main__":
    uvicorn.run(app)
