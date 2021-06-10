# -*- coding: utf-8 -*-

# Zato

from zato.server.service import Service

class GetRecord(Service):
    """Get record from worktribe 
    """
    class SimpleIO:
        input_required = ('record_type', 'record_id')


    def handle(self):
        record_type = self.request.input.record_type
        record_id = self.request.input.record_id
        self.logger.info('record_type : %s',  record_type)
        self.logger.info('record_id : %s',  record_id)
        data = self.invoke(record_type.capitalize(), record_id)
        
        self.response.payload = {
            'Title': data['Title'],
            'ShortTitle': data['ShortTitle']
        }

    def invoke(self, record_type, record_id):
        self.logger.info('Invoking worktribe request; p_id=%s', record_id)
        params= {'record_type':record_type, 'record_id': record_id, 'priority':'normal'}
        # params= {'record_type':'Programme', 'record_id': record_id, 'priority':'normal'}
        self.logger.info('Invoking worktribe with params; %s', params)
        headers = {'Accept': 'application/json'}
        conn = self.outgoing.rest['worktribe.record'].conn
        resp = conn.get(self.cid, params, headers=headers)
        return resp.data


