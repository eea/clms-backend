FROM eeacms/plone:5.2.4-72

COPY site.cfg /plone/instance/
RUN gosu plone buildout -c site.cfg
