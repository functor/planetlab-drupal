#
WEBFETCH := curl -H Pragma: -O -R -S --fail --show-error
SHA1SUM	 := sha1sum

version=4.7.11

ALL		+= drupal
drupal-URL1	:= https://ftp.drupal.org/files/projects/drupal-$(version).tar.gz
drupal-URL2	:= http://mirror.onelab.eu/third-party/drupal-$(version).tar.gz
drupal-SHA1SUM  := c9f767e6c2cd873c4b0bef1986e2821febfc7e34
drupal		:= $(notdir $(drupal-URL1))

ALL		+= taxo
taxo-URL1	:= https://raw.githubusercontent.com/functor/planetlab-third-party/master/taxonomy_block-4.7.x-1.x-dev.tar.gz
taxo-URL1	:= http://build.planet-lab.org/third-party/taxonomy_block-4.7.x-1.x-dev.tar.gz
taxo-URL2	:= http://mirror.onelab.eu/third-party/taxonomy_block-4.7.x-1.x-dev.tar.gz
taxo-SHA1SUM	:= 9d926df1695c0092a74446154b00579d4ccbcb60
taxo		:= $(notdir $(taxo-URL1))

all: $(ALL)
.PHONY: all

##############################
define download_target
$(1): $($(1))
.PHONY: $(1)
$($(1)): 
	@if [ ! -e "$($(1))" ] ; then \
	{ echo Using primary; echo "$(WEBFETCH) $($(1)-URL1)" ; $(WEBFETCH) $($(1)-URL1) ; } || \
	{ echo Using secondary; echo "$(WEBFETCH) $($(1)-URL2)" ; $(WEBFETCH) $($(1)-URL2) ; } ; fi
	@if [ ! -e "$($(1))" ] ; then echo "Could not download source file: $($(1)) does not exist" ; exit 1 ; fi
	@if test "$$$$($(SHA1SUM) $($(1)) | awk '{print $$$$1}')" != "$($(1)-SHA1SUM)" ; then \
	    echo "sha1sum of the downloaded $($(1)) does not match the one from 'Makefile'" ; \
	    echo "Local copy: $$$$($(SHA1SUM) $($(1)))" ; \
	    echo "In Makefile: $($(1)-SHA1SUM)" ; \
	    false ; \
	else \
	    ls -l $($(1)) ; \
	fi
endef

$(eval $(call download_target,drupal))
$(eval $(call download_target,taxo))

sources: $(ALL) 
.PHONY: sources

####################
# default - overridden by the build
SPECFILE = drupal.spec

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
