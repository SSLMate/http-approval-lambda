#
# Copyright (c) 2018 Opsmate, Inc.
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
# Except as contained in this notice, the name(s) of the above copyright
# holders shall not be used in advertising or otherwise to promote the
# sale, use or other dealings in this Software without prior written
# authorization.
#

import base64
import json
import os
import urllib.request

def bad_method():
	return {
		'isBase64Encoded': False,
		'statusCode': 405,
		'statusDescription': '405 Method Not Allowed',
		'headers': {
			'Content-Type': 'text/plain; charset=UTF-8',
			'Allowed': 'GET'
		},
		'body': 'Error: Only the GET method is allowed.'
	}

def bad_gateway(message):
	return {
		'isBase64Encoded': False,
		'statusCode': 502,
		'statusDescription': '502 Bad Gateway',
		'headers': {
			'Content-Type': 'text/plain; charset=UTF-8'
		},
		'body': 'Error contacting SSLMate Approval Proxy: ' + message
	}

def proxy(status_code, status_reason, headers, body):
	return {
		'isBase64Encoded': True,
		'statusCode': status_code,
		'statusDescription': str(status_code) + ' ' + status_reason,
		'headers': headers,
		'body': base64.b64encode(body).decode('utf-8')
	}

def lambda_handler(event, context):
	if event['httpMethod'] != 'GET':
		return bad_method()
	url = os.environ['SSLMATE_HTTP_APPROVAL_PROXY'] + event['path']
	req_headers = {
		'X-Forwarded-Host': event['headers']['host']
	}
	req = urllib.request.Request(url, data=None, headers=req_headers)
	try:
		with urllib.request.urlopen(req) as resp:
			return proxy(resp.status, resp.reason, dict(resp.headers), resp.read())
	except urllib.error.HTTPError as err:
		return proxy(err.status, err.reason, dict(err.headers), err.read())
	except urllib.error.URLError as err:
		return bad_gateway(str(err))
