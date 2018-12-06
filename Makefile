#
# Copyright (c) 2018 Opsmate, Inc.
#
# See COPYING file for license information.
#

VERSION = 0.1.0

all: sslmate_http_approval-$(VERSION).zip template.yaml

sslmate_http_approval-$(VERSION).zip: lambda_function.py
	zip sslmate_http_approval-$(VERSION).zip $^

template.yaml: template.yaml.in Makefile
	m4 -D__VERSION__=$(VERSION) < $< > $@

clean:
	rm -f sslmate_http_approval-*.zip template.yaml

.PHONY: all clean
