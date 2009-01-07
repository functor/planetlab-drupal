# $Id$
CURL	:= curl -H Pragma: -O -R -S --fail --show-error
SHA1SUM	= sha1sum

# default - overridden by the build
SPECFILE = drupal.spec

version=4.7.11

main.URL	:= http://ftp.drupal.org/files/projects/drupal-$(version).tar.gz
main.SHA1SUM    := c9f767e6c2cd873c4b0bef1986e2821febfc7e34

main.FILE	:= $(notdir $(main.URL))

# Thierry - when called from within the build, PWD is /build
SOURCEFILES := $(main.FILE)

$(main.FILE): #FORCE
	@if [ ! -e "$@" ] ; then echo "$(CURL) $(main.URL)" ; $(CURL) $(main.URL) ; fi
	@if [ ! -e "$@" ] ; then echo "Could not download source file: $@ does not exist" ; exit 1 ; fi
	@if test "$$(sha1sum $@ | awk '{print $$1}')" != "$(main.SHA1SUM)" ; then \
	    echo "sha1sum of the downloaded $@ does not match the one from 'sources' file" ; \
	    echo "Local copy: $$(sha1sum $@)" ; \
	    echo "In sources: $(main.SHA1SUM)" ; \
	    exit 1 ; \
	else \
	    ls -l $@ ; \
	fi

sources: $(SOURCEFILES)
.PHONY: sources

PWD=$(shell pwd)
PREPARCH ?= noarch
RPMDIRDEFS = --define "_sourcedir $(PWD)" --define "_builddir $(PWD)" --define "_srcrpmdir $(PWD)" --define "_rpmdir $(PWD)"
trees: sources
	rpmbuild $(RPMDIRDEFS) $(RPMDEFS) --nodeps -bp --target $(PREPARCH) $(SPECFILE)

srpm: sources
	rpmbuild $(RPMDIRDEFS) $(RPMDEFS) --nodeps -bs $(SPECFILE)

TARGET ?= $(shell uname -m)
rpm: sources
	rpmbuild $(RPMDIRDEFS) $(RPMDEFS) --nodeps --target $(TARGET) -bb $(SPECFILE)

clean:
	rm -f *.rpm *.tgz *.bz2 *.gz

++%: varname=$(subst +,,$@)
++%:
	@echo "$(varname)=$($(varname))"
+%: varname=$(subst +,,$@)
+%:
	@echo "$($(varname))"
