FROM eeacms/plonesaas:5.2.7-2

COPY site.cfg /plone/instance/
RUN gosu plone buildout -c site.cfg
