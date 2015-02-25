__author__ = 'ashutosh.banerjee'
from flask import Blueprint, request, redirect, render_template, url_for, jsonify, Response
from flask.views import MethodView
from delmart.models import Shipment, Comment, Credentials
from data_transfer.shipment_dto import ShipmentDto
from mongoengine.fields import *
from delmart.hello import app
from flask import make_response

import json
from bson.json_util import dumps
from bson import json_util
from flask.json import JSONEncoder
import calendar
from datetime import datetime

shipments = Blueprint('shipments', __name__)

# class CustomJSONEncoder(JSONEncoder):
#
#     def default(self, obj):
#         try:
#             if isinstance(obj, datetime):
#                 if obj.utcoffset() is not None:
#                     obj = obj - obj.utcoffset()
#                 millis = int(
#                     calendar.timegm(obj.timetuple()) * 1000 +
#                     obj.microsecond / 1000
#                 )
#                 return millis
#             iterable = iter(obj)
#         except TypeError:
#             pass
#         else:
#             return list(iterable)
#         return JSONEncoder.default(self, obj)


class ListView(MethodView):

    def get(self):
        shipments = Shipment.objects.all()
        format = ShipmentDto(shipments)
        return json.dumps(format.format())
        # return shipments.to_json()
        # return dumps(list(shipments))
        # return jsonify({"shipments":shipments})

    def post(self):
        valid_key = current_user()
        if valid_key = False:
            # return authentication error
        a= {}
        a['shipment_id'] = "1234"
        a['body'] = '16254'
        a['creator_organisation'] = request.json.get('creator_organisation')
        shipment = update_document(Shipment(),a)
        # shipment.creator_organisation = request.json.get('creator_organisation')
        # shipment.body = request.json.get('body')
        shipment.save()
        return Response(shipment, status=200, mimetype='application/json')
        # return json.dumps({"z":1})

class DetailView(MethodView):

    def get(self, shipment_id):
        shipments = Shipment.objects.get_or_404(shipment_id=shipment_id)
        return shipments


def Authenticate():
    request_key = request.json.get('authentication_key');
    if Credentials.objects(key=request_key):
        return True 
    else :
        return False

def field_value(field, value):
  '''
  Converts a supplied value to the type required by the field.
  If the field requires a EmbeddedDocument the EmbeddedDocument
  is created and updated using the supplied data.
  '''
  if field.__class__ in (ListField, SortedListField):
    # return a list of the field values
    return [
      field_value(field.field, item)
      for item in value]

  elif field.__class__ in (
    EmbeddedDocumentField,
    GenericEmbeddedDocumentField,
    ReferenceField,
    GenericReferenceField):

    embedded_doc = field.document_type()
    update_document(embedded_doc, value)
    return embedded_doc
  else:
    return value


def update_document(doc, data):
  ''' Update an document to match the supplied dictionary.
  '''
  for key, value in data.iteritems():

    if hasattr(doc, key):
        value = field_value(doc._fields[key], value)
        setattr(doc, key, value)
    else:
        # handle invalid key
        pass

  return doc

shipments.add_url_rule('/', view_func=ListView.as_view('list'))
shipments.add_url_rule('/<shipment_id>/', view_func=DetailView.as_view('detail'))

@app.route('/register', methods=('GET', 'POST'))
def register():
  if request.method == 'POST':
    username = request.form.get('username')
	  key = request.form.get('key')
    #other fields
    credential = Credentials(username = username, key = key);
    credential.save();
  else:
    # Registration form

