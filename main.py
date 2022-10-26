import csv
import re
from collections import Counter, defaultdict


class AddressBookCorrector:

    def __init__(self, input_path, output_path):
        self.input_path = input_path
        self.output_path = output_path

        self.phone_pattern = r'^(\+7|8)\s?\(?(\d{0,3})\)?\s?-?(\d{0,3})-?' \
                             r'(\d{0,2})-?(\d{0,2}) ?\(?(\w{0,3}[.]?) ?(\d{0,4})\)?'
        self.repl = r'+7(\2)\3‐\4‐\5 \6\7'

        self.contacts_list = None

    def _read_data(self):
        with open(self.input_path) as f:
            rows = csv.reader(f, delimiter=',')
            self.contacts_list = list(rows)

    def _write_data(self):
        with open(self.output_path, 'w') as f:
            datawriter = csv.writer(f, delimiter=',')
            datawriter.writerows(self.contacts_list)

    def _correct_data(self):
        headers = self.contacts_list.pop(0)

        for contact in self.contacts_list:
            lastname = re.findall(r'\w+', contact[0])
            firstname = re.findall(r'\w+', contact[1])

            if len(lastname) == 2:
                contact[0] = lastname[0]
                contact[1] = lastname[1]

            if len(lastname) == 3:
                contact[0] = lastname[0]
                contact[1] = lastname[1]
                contact[2] = lastname[2]

            if len(firstname) == 2:
                contact[1] = firstname[0]
                contact[2] = firstname[1]

            contact[5] = re.sub(self.phone_pattern, self.repl, contact[5]).rstrip()

        matches = dict(Counter([contact[0] for contact in self.contacts_list]))
        matches = [match[0] for match in matches.items() if match[1] > 1]

        duples = [self.contacts_list.pop(i) for i, contact in enumerate(self.contacts_list) if contact[0] in matches]

        united = defaultdict(list)
        for dupl in duples:
            key = tuple(dupl[:2])
            for item in dupl:
                if item not in united[key]:
                    united[key].append(item)
        united = list(united.values())

        self.contacts_list.extend(united)
        self.contacts_list.insert(0, headers)

    def correct(self):
        self._read_data()
        self._correct_data()
        self._write_data()

        print(f'Данные успешно откорректированы и загружены в файл: {self.output_path}!')


if __name__ == '__main__':
    corrector = AddressBookCorrector(input_path='phonebook_raw.csv', output_path='phonebook.csv')
    corrector.correct()
