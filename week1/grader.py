import requests
import json
import numpy as np
from collections import OrderedDict

class Grader(object):
    def __init__(self):
        self.submission_page = 'https://www.coursera.org/api/onDemandProgrammingScriptSubmissions.v1'
        self.assignment_key = 'MSsYBMLgEeesWhJPHRLG5g'
        self.parts = OrderedDict([('f5nXa', 'TextPrepare'), 
                                  ('hTrz8', 'WordsTagsCount'), 
                                  ('0kUjR', 'BagOfWords'), 
                                  ('tLJV1', 'MultilabelClassification')])
        self.answers = {key: None for key in self.parts}

    @staticmethod
    def ravel_output(output):
        '''
           If student accidentally submitted np.array with one
           element instead of number, this function will submit
           this number instead
        '''
        if isinstance(output, np.ndarray) and output.size == 1:
            output = output.item(0)
        return output

    def submit(self, email, token):
        submission = {
                    "assignmentKey": self.assignment_key, 
                    "submitterEmail": email, 
                    "secret": token, 
                    "parts": {}
                  }
        for part, output in self.answers.items():
            submission["parts"][part] = {"output": output} if output is not None else {}
        request = requests.post(self.submission_page, data=json.dumps(submission))
        response = request.json()
        if request.status_code == 201:
            print('Submitted to Coursera platform. See results on assignment page!')
        elif u'details' in response and u'learnerMessage' in response[u'details']:
            print(response[u'details'][u'learnerMessage'])
        else:
            print(f"Unknown response from Coursera: {request.status_code}")
            print(response)

    def status(self):
        print("You want to submit these parts:")
        for part_id, part_name in self.parts.items():
            answer = self.answers[part_id]
            if answer is None:
                answer = '-'*10
            print(f"Task {part_name}:\n {answer[:100]}...")
               
    def submit_part(self, part, output):
        self.answers[part] = output
        print(f"Current answer for task {self.parts[part]} is:\n {output[:100]}...")

    def submit_tag(self, tag, output):
        part_id = [k for k, v in self.parts.items() if v == tag]
        if len(part_id) != 1:
            raise RuntimeError(
                f'cannot match tag with part_id: found {len(part_id)} matches'
            )
        part_id = part_id[0]
        self.submit_part(part_id, str(self.ravel_output(output)))
