from nltk.tokenize import TreebankWordTokenizer
from nltk.wsd import lesk
from nltk.corpus import wordnet as wn
import os
from unidecode import unidecode

print (os.getcwd())

# ['als', 'arb', 'cat', 'cmn', 'dan', 'eng', 'eus', 'fas',
# 'fin', 'fra', 'fre', 'glg', 'heb', 'ind', 'ita', 'jpn', 'nno',
# 'nob', 'pol', 'por', 'spa', 'tha', 'zsm']
lang='fra'


def get_synonyms(word:str, pos:str) -> list :
    """Generate the synset associated to a word

    Args:
        word (str): word on wich you want the syn list
        pos (str): 'a' 'b' 'v' '?' of TOFINISH

    Returns:
        list: List of synonyms 
    """
    synonyms = set()
    for synset in wn.synsets(word, pos = pos, lang='fra'):
        for lemma in synset.lemmas('fra') :
            synonyms.add(lemma)#.name())
    return synonyms


def generate_wordnet_format(word_id:int, syn_num:int, word:str, pos:str) ->str :
    """Generate the wordnet format for the given parameters

    Args:
        word_id (int): the synset ID 
        syn_num (int): number of synonym
        word (str): the word
        pos (str): pos

    Returns:
        str: wordnet format
    """
    return f"s({word_id}, {syn_num}, '{word}', {pos}, 1, 0).\n"

def generate_synset(syn_id:int, syn_list:list, stop_words:list, pos:str, lemma_c:str) -> str: 
    already_put = []
    synset = ""
    c=1
    for syn in syn_list : 
        if syn.name() not in stop_words : 
            syn = unidecode(syn.name().lower())
            if (syn != lemma_c) :
                if syn not in already_put :  
                    if not syn_to_be_removed(syn, syn_list) :
                        already_put.append(syn)
                        c+=1
                        synset += generate_wordnet_format(syn_id, c, syn, pos)
    return synset
        


def lemma_to_be_removed(lemma:str) -> bool : 
    regex_numbers = ["dix", "vingt", "trente", "quarante", "cinquante", "soixante", "cent"]
    if lemma in regex_numbers : 
        return True 
    for r in regex_numbers :
        if r in lemma and '-' in lemma : 
            return True
    if lemma.isdigit() :
        return True
    
    return False

def test_to_be_removed() : 
    print(f'Lemma : trente -> {lemma_to_be_removed("trente")}')
    print(f'Lemma : quarante-cinq -> {lemma_to_be_removed("quarante-cinq")}')
    print(f'Lemma : ali_baba_et_les_quarante_voleurs -> {lemma_to_be_removed("ali_baba_et_les_quarante_voleurs")}')
    print(f'Lemma : trente -> {lemma_to_be_removed("trente")}')
    print(f'Lemma : 5 -> {lemma_to_be_removed("5")}')


def syn_to_be_removed(syn, syn_list) :
    if len(syn) < 3 : return True
    regex_numbers = ["dix", "vingt", "trente", "quarante", "cinquante", "soixante", "cent"]
    if syn in regex_numbers : 
        return True 
    for r in regex_numbers :
        if r in syn and '-' in syn : 
            return True
    if syn.isdigit() :
        return True

    return False



def extract_synonyms_to_file(stop_words=[]):
    lang = 'fra'
    word_id = 1
    with open(f'output/{lang}_synonyms_wordnet_format.txt', 'w', encoding='utf-8') as file:
        for lemma in wn.all_lemma_names(lang=lang):
            if lemma not in stop_words:
                pos_syn = wn.synsets(lemma, lang='fra')[0].pos()
                synonyms = get_synonyms(lemma, pos_syn)
                c = 1
                lemma_c = unidecode(lemma.lower())
                if len(synonyms) > 2  and len(synonyms) < 12 and pos_syn not in ['r', 's'] and not lemma_to_be_removed(lemma) :
                    file.write(generate_wordnet_format(word_id, 1, lemma_c, pos_syn))
                    file.write(generate_synset(word_id, synonyms, stop_words, pos_syn, lemma_c))
                    word_id += 1
                    
#test_to_be_removed()
stop_words = open("stopword/stopword_fr.txt").read().splitlines()
#['le', 'la', 'de', 'et', 'à', 'est']
extract_synonyms_to_file(stop_words)
