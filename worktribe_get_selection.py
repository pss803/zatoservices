# -*- coding: utf-8 -*-

# Zato

from zato.server.service import Service

class GetSelections(Service):
    """Get record from worktribe 
    """
    class SimpleIO:
        input_required = ('selection_id')


    def handle(self):
        selection_id = self.request.input.selection_id
        self.logger.info('selection_id : %s',  selection_id)
        data = self.invoke(selection_id)
        result_list=[]
        for result in data['Results']:
            record={}
            record['Title']=result['Title']
            record['ProgrammeCode']=result['ProgrammeCode']
            record['id']=result['_self']['ID']
            result_list.append(record)
        self.response.payload = {
            'Title': data['Title'],
            'Description': data['Description'],
            'Results': result_list
        }

    def invoke(self, selection_id):
        self.logger.info('Invoking worktribe selection; p_id=%s', selection_id)
        params= {'selection_id': selection_id, 'priority':'normal'}
        headers = {'Accept': 'application/json'}
        conn = self.outgoing.rest['worktribe.selections'].conn
        resp = conn.get(self.cid, params, headers=headers)
        return resp.data