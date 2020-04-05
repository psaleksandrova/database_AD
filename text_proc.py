import bs4
from bs4 import BeautifulSoup


def check_style(tag):
    if tag.endswith('BoldMT'):
        return 'b'
    if tag.endswith('ItalicMT'):
        return 'i'
    # if tag.endswith("RomanPSMT"):
    # return 'u'


def get_dict(path):
    # деление текста на слова, создание словаря
    # path - путь до файла в формате xml, где лежит результат обработки pdfminer
    with open(path, encoding="utf-8") as r:
        soup = BeautifulSoup(r)
        # смена слова - жирный капс
        # 8.000 - синопсис
        items = soup.find_all('text')
        word = []
        word_tagged = []
        c = 0
        flag = 0
        prew = ''
        d = {}
        d_tagged = {}
        for item in items:
            s_tag = item.attrs.get('size')
            f_tag = item.attrs.get('font')
            try:
                curr = check_style(f_tag)
                if prew == curr:
                    prew = curr
                elif prew != '':
                    if curr is None and prew is not None:
                        the_line = '</{0}>'.format(prew)
                    elif curr is not None:
                        if prew is None:
                            the_line = '<{0}>'.format(curr)
                        else:
                            the_line = '</{0}><{1}>'.format(prew, curr)
                    word_tagged.append(the_line)
                prew = curr
            except:
                continue
            try:
                w = item.text
            except:
                w = ' '
            if s_tag == '9.000' and f_tag == 'NFDIBK+TimesNewRomanPS-BoldMT' and w.isupper() is True:
                if c == 0:
                    word.append(w)
                    word_tagged.append(w)
                else:
                    # но главная проблема - подчеркивание - возможно список помет
                    ch = ''.join(word)
                    if flag == 0:
                        word.append(w)
                        word_tagged.append(w)
                    elif flag == 1:
                        if ch.isupper() is True:
                            word.append(w)
                            word_tagged.append(w)
                        else:
                            flag = 0
                            word = ''.join(word)
                            word_tagged = ''.join(word_tagged)
                            word_tagged = '<b>' + word_tagged
                            d[c] = word
                            d_tagged[c] = word_tagged
                            c += 1
                            word = []
                            word_tagged = []
                            word.append(w)
                            word_tagged.append(w)
            else:
                if s_tag == '9.000' or s_tag == '8.000':
                    flag = 1
                    if c == 0:
                        c += 1
                    word.append(w)
                    word_tagged.append(w)
                else:
                    continue
    return d, d_tagged


def dividing(d, d_tagged):
    lexem = 0
    pos = 0
    gram = 0
    rest = 0
    for key, value in d.items():
        # p = value.split('.')
        p = value.partition('.')
        # p = value.split('.', 1)[-1]
        rest = p[2]
        q = p[0].split(';')
        e = q[0].split(',')
        lexem = e[0]
        try:
            index = key
            lexem = e[0]
            pos = e[1]
            gram = q[1]
            tagged = d_tagged[key]
            # to_json = {'lexem': lexem, 'pos': pos, 'gram': gram, 'rest': rest}
            # with open('as.json', 'a') as f:
            # json.dump(to_json, f, sort_keys=True, indent=2)
            print(index)
            print(e[0])
            print(e[1])
            print(q[1])
            print(rest)
            print(tagged)
        except:
            # для случаев типа "абордаж"
            print(key)
            print(value)


def split_val(n, d, d_tagged):
    soup = BeautifulSoup(d_tagged[n])
    b = soup.find_all('b')
    meanings = []
    for item in b:
        if item.text != '':
            if item.text[-1].isdigit():
                meanings.append(item.text)
    meaning_check = meanings[0].split(' ')[0]
    print(meaning_check)
    meanings = [mc for mc in meanings if mc.startswith(meaning_check)]
    print(meanings)
    parted = []
    k = d[n]
    for m in meanings:
        if len(parted) != 0:
            k = k.partition(m)
            flag = k[0]
            k = k[2]
            parted.append(flag)
            parted.append(m)
            # parted.append(k)
        else:
            k = k.partition(m)
            k = k[2]
            parted.append(m)
    parted.append(k)
    return parted


def main():
    path = 'res.xml'
    d, d_tagged = get_dict(path)
    dividing(d, d_tagged)
    n = int(input())
    parted = split_val(n, d, d_tagged)
    print(parted)


if __name__ == "__main__":
    main()
