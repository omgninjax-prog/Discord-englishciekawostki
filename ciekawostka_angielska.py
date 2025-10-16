# -*- coding: utf-8 -*-
"""
english_facts.py
Put in your repo and run with DISCORD_WEBHOOK_URL environment variable set
(GitHub Actions: export DISCORD_WEBHOOK_URL="${{ secrets.ENGLISH_WEBHOOK }}")
Script chooses a yearly permutation (seed = year) and sends the fact corresponding to the day of year.
Requires: requests
"""

import os
import datetime
import json
import requests
import random
import sys

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL", "")

# Small pools to programmatically build 365 readable English facts about the language.
starters = [
    "Did you know", "Fun fact", "Language note", "Quick fact", "Word trivia",
    "Pronunciation tip", "Grammar note", "Etymology insight", "Vocabulary fact",
    "Historical note"
]

english_topics = [
    "word origins", "spelling quirks", "idioms", "phrasal verbs", "pronunciation",
    "grammar", "slang", "loanwords", "false friends", "word families",
    "register", "punctuation", "collocations", "etymology", "rhymes"
]

short_facts_base = [
 [
"Słowo 'set' ma jedno z największych liczebnie znaczeń w języku angielskim — ponad 400 znaczeń.",
"Słowo 'alphabet' pochodzi od pierwszych liter alfabetu fenickiego: 'aleph' i 'beth'.",
"Angielski ma wiele zapożyczeń — słowa z łaciny, francuskiego, greki i innych języków.",
"Najdłuższe słowo w słowniku to często 'pneumonoultramicroscopicsilicovolcanoconiosis'.",
"Angielski nie ma jednej instytucji normującej (jak Akademia) — zmiany następują ewolucyjnie.",
"Słowo 'nice' kiedyś znaczące 'głupi' — znaczenie zmieniło się z biegiem czasu.",
"Letter 'J' pojawiła się później w alfabecie łacińskim; wcześniej używano 'I' do dźwięku j.",
"Irregular verbs (czasowniki nieregularne) pamiętają dawną historię języka.",
"Słowo 'goodbye' pochodzi z 'God be with ye' — skurcz frazy.",
"Angielski globalnie ma wiele odmian: brytyjska, amerykańska, australijska, indyjskie angielskie itd.",
"Homofony to słowa brzmiące tak samo, ale pisane inaczej: 'there', 'their', 'they're'.",
"Najczęściej używane słowa w angielskim to 'the', 'be', 'to', 'of', 'and'.",
"Spelling 'ghoti' to żart pokazujący nieregularność angielskiej ortografii (fish -> ghoti).",
"Angielski ma wiele idiomów: 'break the ice' oznacza przełamać niezręczność.",
"Phrasal verbs (verb + particle) są bardzo powszechne i często idiomatyczne.",
"Longest one-syllable word in English is often considered 'screeched'.",
"Angielski używa artykułów 'a/an' i 'the' — pierwszeństwo kontekstu decyduje o wyborze.",
"Angielski ma wiele czasów gramatycznych, w tym konstrukcje perfect i continuous.",
"Słowo 'quiz' prawdopodobnie pochodzi z XVIII-wiecznego żartu — źródło niepewne.",
"Etymologia słowa może ujawnić jego historię i zmiany znaczeń.",
"Anagram to przestawienie liter: 'listen' -> 'silent'.",
"Palindromy czytane odwrotnie dają ten sam zapis: 'level', 'racecar'.",
"Brytyjczycy używają 'lorry' tam gdzie Amerykanie 'truck'.",
"Słowo 'salary' pochodzi od łacińskiego 'salarium' — opłaty w soli w starożytności.",
"Pronunciation (wymowa) często różni się od zapisu — 'ough' ma wiele wersji (though, cough...).",
"Oxymoron łączy sprzeczne pojęcia: 'deafening silence'.",
"Idiomy kulturowe często nie tłumaczą się dosłownie.",
"Angielski intensywnie upraszcza fleksję (mniej końcówek niż łacina).",
"Collocations to typowe zestawienia słów: 'make a decision', 'do homework'.",
"False friends to słowa podobne do polskich, ale inne znaczenie: 'actual' ≠ 'aktualny' (oznacza 'rzeczywisty').",
"Compound words łączą dwa słowa: 'toothbrush', 'sunflower'.",
"Angielski ma silne i słabe formy wyrażeń (np. 'a' vs 'an' przy wymowie).",
"Suffix '-ness' tworzy rzeczowniki od przymiotników: 'happiness'.",
"Prefix 'un-' tworzy zaprzeczenia: 'unknown'.",
"Modal verbs (can, could, may, might) wyrażają możliwość i pozwolenie.",
"Rhyming: poezja angielska często opiera się na rymach i rytmie (meter).",
"Onomatopoeia: words that imitate sounds — 'buzz', 'buzz', 'splash'.",
"Angielski słownictwo poszerza się przez nowe technologie i kulturę (np. 'google' jako czasownik).",
"Fixed expressions (chunks) pomagają brzmieć naturalnie: 'How's it going?'.",
"Conditional sentences: zero, first, second, third conditionals opisują realne/nierealne sytuacje.",
"Loanwords z języka francuskiego (np. 'government', 'justice') po Normandii.",
"Synonyms to wyrazy o podobnym znaczeniu; wybór często zależy od stylu.",
"Register językowy: formalny vs nieformalny — dobieraj słowa do sytuacji.",
"Word stress (akcent wyrazowy) w angielskim może zmieniać znaczenie: 'record (n)' vs 'record (v)'.",
"Suffix '-ly' tworzy przysłówki od przymiotników: 'quick' -> 'quickly'.",
"Clipping skraca słowa: 'phone' od 'telephone'.",
"Portmanteau łączy dwa słowa: 'brunch' = breakfast + lunch.",
"Double negatives w standardowym angielskim są niepoprawne: 'I don't know nothing' → błędne.",
"Regular verbs tworzą past simple przez dodanie -ed: 'walk' -> 'walked'.",
"Angielska intonacja może zmieniać znaczenie zdania (np. pytanie vs stwierdzenie).",
"Countable vs uncountable nouns: 'apple' policzalne, 'information' niepoliczalne.",
"Prefixes and suffixes pomagają rozszerzać słownictwo bez zapamiętywania nowych rdzeni.",
"Etymologia słowa 'salary' związana z solą i wynagrodzeniem rzymskich żołnierzy.",
"Homographs — takie same pisownie, różna wymowa i znaczenie: 'lead' (prowadzić) vs 'lead' (ołów).",
"Angielskie liczby porządkowe: 1st (first), 2nd (second), 3rd (third).",
"Sentence connectors (however, therefore, moreover) łączą idee w tekście.",
"Reductions w mowie potocznej redukują sylaby: 'gonna' od 'going to'.",
"English spelling reformy były proponowane, ale standard utrzymano przez konwencję.",
"False friends: 'actually' nie znaczy 'aktualnie', lecz 'w rzeczywistości'.",
"Idiomy z jedzeniem: 'piece of cake' = coś łatwego.",
"Speech acts: pytania, prośby, rozkazy — różne funkcje wypowiedzi.",
"British vs American spelling: 'colour' (UK) vs 'color' (US).",
"Compound adjectives mogą być łączone myślnikiem: 'well-known author'.",
"Subjunctive mood używany rzadziej, ale istnieje: 'If I were you...'.",
"Toponyms: nazwy miejsc wpływają na słownictwo (np. 'sandwich' od nazwiska Earl of Sandwich).",
"Word formation: derivation, compounding, conversion (zmiana części mowy bez zmiany formy).",
"Linking sounds łączą słowa w mowie: 'an apple' wymawia się płynnie.",
"Stress-timed rhythm vs syllable-timed rhythm: angielski ma tendencję stress-timed.",
"Minimal pairs pokazują różnice fonetyczne: 'ship' vs 'sheep'.",
"English has many dialectal vowel shifts (np. Northern vs Southern accents).",
"Register: 'children' (neutral) vs 'kids' (nieformalne).",
"English uses phrasal verbs intensively: 'look after', 'run into', 'get by'.",
"Countable nouns use 'many', uncountable use 'much'.",
"Word order (SVO) — angielski ma zazwyczaj kolejność Subject-Verb-Object.",
"Suffix '-able' oznacza możliwość: 'readable' = możliwe do przeczytania.",
"Modal perfect: 'should have done' do mówienia o żalu/oczekiwaniu.",
"Collocations: 'heavy rain' (nie 'strong rain').",
"Abbreviations: 'etc.' = et cetera, 'e.g.' = for example (exempli gratia).",
"Loanwords z niemieckiego: 'kindergarten'.",
"Compound nouns mogą zmieniać akcent w zależności od funkcji: 'greenhouse' vs 'green house'.",
"Ellipsis allows omitting elementów w kontekście: 'I will, if you will (too)'.",
"Tag questions: 'It's nice, isn't it?' — używane do potwierdzenia opinii.",
"Pronunciation differences can indicate regional origin in native speakers.",
"False cognates: 'actual' (EN) ≠ 'aktualny' (PL).",
"Contractions are common w mowie: 'I'm', 'you're', 'they've'.",
"Derivational morphemes change word class: 'beauty' (n) -> 'beautiful' (adj).",
"Prefixes negative: 'dis-', 'in-', 'un-' tworzą zaprzeczenia.",
"Register in writing: academic writing avoids contractions and slang.",
"English proverbs: 'A stitch in time saves nine' — mądrości kulturowe.",
"Loanwords from Latin in scientific vocabulary: 'aquatic', 'biology'.",
"Pronouns: subject (I, you) vs object (me, you).",
"Reported speech changes tense after reporting verb in past: 'She said she was tired.'",
"English has many particle verbs where particle zmienia znaczenie czasownika.",
"Word order changes in questions: auxiliary verb comes before subject: 'Do you like it?'.",
"Subordination vs coordination: because (subordinating), and/but (coordinating).",
"Phrase 'to bite the bullet' — idiom meaning 'zebrać się na odwagę'.",
"English sentences can be simple, compound, complex or compound-complex.",
"Link between pronunciation and spelling is weak — trzeba trenować wymowę.",
"Derivational suffixes often zmieniają część mowy: 'decide'->'decision'.",
"Affixation is a major way of tworzenia nowych słów w angielskim.",
"Headword w słowniku podaje podstawową formę słowa.",
"Register changes: 'inquire' (formal) vs 'ask' (neutral).",
"Passive voice: 'The cake was eaten' — używamy, gdy aktor jest nieznany lub nieistotny.",
"Gerunds vs infinitives: 'I like swimming' vs 'I like to swim' — subtelne różnice.",
"Compound prepositions: 'in front of', 'next to'.",
"Word frequency lists pomagają uczyć się najważniejszych słów pierwszych.",
"False friends include 'sympathy' (EN) vs 'sympatia' (PL) — różne znaczenia.",
"Idioms często mają historyczne lub kulturowe źródła.",
"English calendar words: 'Wednesday' pochodzi od imienia boga nordyckiego Wodena (Odin).",
"Suffix '-ist' tworzy nazwiska zawodów/ideologii: 'artist', 'scientist'.",
"Collocations: 'heavy traffic' not 'strong traffic'.",
"Compound adjectives with numbers: 'a 3-year-old child' (z myślnikiem).",
"Prefixes 're-' oznacza powtórzenie: 'redo' = zrobić ponownie.",
"Reported questions invert order and use 'if/whether': 'He asked if I was coming.'",
"Imperatives (rozkaźnik) często pomijają podmiot: 'Sit down.'",
"Echo questions repeat część wypowiedzi: 'You saw what?'.",
"English has many idiomatic phrasal verbs that nie zawsze łatwo tłumaczyć dosłownie.",
"Word families help zapamiętywać: 'teach, teacher, teaching'.",
"Suffix '-tion' tworzy rzeczowniki od czasowników: 'inspire' -> 'inspiration'.",
"Linking R w wielu akcentach (non-rhotic vs rhotic accents) wpływa na wymowę.",
"Stress patterns can wskazywać klasę słowotwórczą: REcord (n) vs reCORD (v).",
"Borrowings from Spanish in American English: 'patio', 'canyon'.",
"Conventional spelling sometimes zachowuje historyczne elementy, np. 'knight'.",
"Minimal pairs are kluczowe przy nauce poprawnej wymowy.",
"Synonymy rarely pełna — słowa rzadko są idealnymi synonimami.",
"Prefix 'mis-' oznacza coś robić źle: 'misunderstand'.",
"English uses many fixed expressions w mowie potocznej: 'at the end of the day'.",
"Word 'sir' and 'madam' used as polite forms of address in formal contexts.",
"Conditional sentences type 3 mówią o przeszłości nierealnej: 'If I had known, I would have come.'",
"Emphatic do: 'I do like it!' używane do wzmocnienia twierdzenia.",
"Loanwords z języka hindi w angielskim: 'pyjamas' (UK 'pajamas' US).",
"Derivation vs inflection: derivation tworzy nowe słowa, inflection zmienia formę gramatyczną.",
"Genre-specific lexis: academic English ma swoje typowe słownictwo.",
"Tag questions mogą być użyte do prośby o potwierdzenie lub uprzejmości.",
"Capitalization rules: nazwy własne, początek zdania, 'I' zawsze wielkie.",
"Suffix '-hood' tworzy rzeczowniki abstrakcyjne: 'childhood'.",
"Contractions formalność: lepiej ich unikać w formalnym piśmie.",
"Prefixes 'pre-' (przed), 'post-' (po) pomagają budować określenia czasowe.",
"Direct speech vs reported speech — zmiana cudzysłowów i czasów.",
"Word order in adjectives: opinion-size-age-shape-color-origin-material-purpose (dla wielu adj).",
"English has many irregular plurals: 'child'->'children', 'mouse'->'mice'.",
"False friends: 'eventually' (EN) ≠ 'ewentualnie' (PL) — 'eventually' = 'w końcu'.",
"Pronunciation of 'th' może być dental voiced (/ð/) jak w 'this' lub voiceless (/θ/) jak w 'think'.",
"Contrastive stress może zmieniać znaczenie: 'I didn't say he stole the money' (w zależności od akcentowane słowa).",
"Rhyming slang (Cockney) to zabawna gra językowa: 'apples and pears' = stairs.",
"Suffix '-ship' tworzy rzeczowniki stanu: 'friendship'.",
"Conversion (zero-derivation) zmienia kategorię słowa bez zmiany formy: 'to run' (v) -> 'a run' (n).",
"Infinitive with 'to' vs bare infinitive after modal verbs: 'can go' vs 'to go'.",
"Passive with 'get' ('He got arrested') jest nieformalne i oznacza skutek.",
"Fronting w zdaniu służy do zaakcentowania elementu: 'Never have I seen...' ",
"English orthography historically preserved dawne wymawianie (np. 'kn' leading consonant cluster).",
"Lexical set: zestaw słów o podobnych fonetycznych cechach (używane w fonetyce).",
"Pronunciation of vowels varies widely across accents — np. 'bath' in UK vs US.",
"Compound nouns sometimes pisane razem lub oddzielnie w zależności od zwyczaju.",
"Nominalization converts verbs/adjectives to nouns: 'decide' -> 'decision'.",
"Relative clauses mogą być defining (ograniczające) i non-defining (dodatkowe).",
"Indirect questions są grzeczniejsze: 'Could you tell me where the station is?'",
"English politeness strategies: modal verbs, softeners ('perhaps', 'maybe').",
"Inversion używane w formalnym stylu: 'Rarely have I seen...' ",
"Suffix '-ize' tworzy czasowniki: 'modernize'.",
"Stress in multi-syllable nouns often on antepenultimate or penultimate syllable w zależności od słowotwórstwa.",
"Comparatives and superlatives: 'big', 'bigger', 'biggest' or 'more interesting'.",
"Tag questions forms zależą od operatora w zdaniu głównym i polarity.",
"Word building through combining forms: 'bio-' (life), 'geo-' (earth).",
"False friends: 'actual' vs 'aktualny' — 'actual' znaczy 'faktyczny'.",
"Pronunciation practice: shadowing (powtarzanie za native speakerem) pomaga płynności.",
"English prose styles vary: journalistic vs academic vs creative writing.",
"Intonation patterns include rising, falling, fall-rise — różne funkcje pragmatyczne.",
"Ellipsis w mowie: 'Want some?' zamiast 'Do you want some?'.",
"Stress-timed rhythm means sylaby bezstresowe są krótsze, a stresowane wydłużone.",
"English blends / portmanteau words: 'smog' = smoke + fog.",
"Conjunctions help łączyć klauzule i idee: 'although', 'while', 'since'.",
"British idioms vs American idioms często różnią się semantyką i użyciem.",
"Clipped forms e.g. 'info' (information) są powszechne w mowie potocznej.",
"Pronunciation: voiced vs voiceless consonants change brzmienie (e.g., b vs p).",
"Phonemes vs graphemes: dźwięki vs litery — nie zawsze jednoznaczne dopasowanie.",
"Minimal pair exercise: 'bat' vs 'pat' helps distinguish /b/ and /p/.",
"Rhotic vs non-rhotic accent: whether 'r' is pronounced after vowels (US vs many UK accents).",
"Compound adjective hyphenation: 'a well-known artist' — używamy myślnika.",
"English has many phrasal verbs with multiple meanings: 'pick up' może znaczyć 'podnieść' lub 'odebrać'.",
"Derivational morphology often zmienia strefę akcentu w wyrazie.",
"False friends: 'sympathetic' (EN) ≠ 'sympatyczny' (PL) — 'sympathetic' = 'życzliwy, współczujący'.",
"Loanwords from French: 'restaurant', 'ballet'.",
"Pronunciation differences can mark social/regional identity.",
"Register and tone w komunikacji pisemnej wpływają na dobór słownictwa.",
"Compound verbs are mniej formalne i powszechne w mowie.",
"English uses articles differently niż polski — trzeba ćwiczyć z kontekstem.",
"Suffix '-ee' oznacza osobę doświadczającą czegoś: 'employee'.",
"Word stress and sentence stress różnią się: sentence stress podkreśla najważniejsze informacje.",
"Question tags mogą być użyte do prośby o potwierdzenie: 'You like coffee, don't you?'.",
"Derivational vs inflectional morphemes: inflectional zmienia gramatykę (np. -s plural).",
"Loanwords from Dutch: 'cookie' (from 'koekje').",
"Use of articles: 'in hospital' (BrE) vs 'in the hospital' (AmE) — różnice regionalne.",
"Fixed collocations ważne dla płynności: 'make a decision', not 'do a decision'.",
"English has many multi-word verbs; ucz się je w kontekście.",
"British idiomatic expressions often mają historyczne pochodzenie.",
"Pronouns 'who' for people, 'which' for things (relative clauses).",
"Suffix '-able' often forms adjectives meaning 'możliwość': 'readable'.",
"Breve and macron are symbolami používanými v fonetyce by pokazać długość samogłoski.",
"Homophones can prowadzić do ortograficznych błędów: 'to', 'too', 'two'.",
"Register: sleng to część mowy potocznej, avoid in formal contexts.",
"Modal verbs behave differently w różnych strukturach (np. perfect forms).",
"English poetry meters: iambic pentameter is common in Shakespeare.",
"Collocations ćwiczą naturalne użycie: 'make progress', nie 'do progress'.",
"Phrase verbs mogą mieć separable i inseparable forms (e.g., 'turn off the light' vs 'turn the light off').",
"Suffix '-ism' tworzy nazwy ideologii: 'capitalism'.",
"Compound nouns sometimes have main stress on first element: 'GREENhouse' vs 'green HOUSE' różne znaczenia.",
"Idioms często odzwierciedlają kulturę i dawne praktyki.",
"Loanwords from Arabic: 'alchemy', 'algebra' — wpływ kultury islamskiej na naukę.",
"Prefixes 'inter-', 'intra-' oznaczają między i wewnątrz: 'international' vs 'intramural'.",
"English has wiele żartobliwych gier słownych, np. puns (kalambury).",
"Pronunciation training: minimal pairs i shadowing to efektywne techniki.",
"Suffix '-able' vs '-ible': reguły często historyczne i nieintuicyjne.",
"Word order exceptions: emphatic fronting or inversion for stylu.",
"False friends: 'eventually' vs 'ewentualnie' — watch out!",
"Homonyms — same spelling and pronunciation, różne znaczenia: 'bat' (zwierzę) i 'bat' (do baseballu).",
"Compare British and American vocabulary: 'holiday' (UK) = 'vacation' (US).",
"Inflection in English jest ograniczona w porównaniu do języków fleksyjnych.",
"Pragmatics bada znaczenie kontekstowe and implicature — o co ktoś naprawdę chodzi.",
"Derivation często zmienia akcent: 'photograph' (n) vs 'photographic' (adj).",
"English word stress often affects vowel reduction w sylabach bezstresowych.",
"Conditionals: mixed conditionals używają różnych czasów do opisywania złożonych sytuacji.",
"Pronunciation of vowels w angielskim różni się bardziej niż w wielu innych językach.",
"Word families i listy frekwencyjne to efektywny sposób uczenia słownictwa.",
"Particles in phrasal verbs mogą zmieniać znaczenie drastycznie (e.g., 'take off' vs 'take on').",
"Suffix '-ful' tworzy przymiotniki: 'hopeful' = pełen nadziei.",
"Contrastive stress może sygnalizować kontrast między elementami zdania.",
"Politeness strategies: hedging ('maybe', 'perhaps') używane by złagodzić wypowiedź.",
"English vowels have różne alofony depending on accent and context.",
"British Received Pronunciation (RP) był tradycyjnym wzorcem wymowy, lecz nie jedynym.",
"Word formation przez compounding jest produktywna: 'bookshop', 'toothpaste'.",
"False friends: 'library' (EN) ≠ 'libra ry' (PL) — 'library' = biblioteka.",
"Lexical bundles to typowe frazy używane w akademickim angielskim.",
"English is a Germanic language with dużą warstwą leksykalną łacińsko-romanską.",
"Suffix '-less' tworzy przeczenia: 'hopeless'.",
"Pragmatic markers like 'you know' lub 'I mean' pełnią funkcje społeczne w rozmowie.",
"Homophones mogą być źródłem żartów i kalamburów.",
"British and American punctuation rules mogą się różnić (np. użycie cudzysłowów).",
"English lexis includes many compound terms in technicznych dziedzinach.",
"Word stress and intonation są kluczowe dla zrozumiałości i naturalności.",
"Historic sound changes (Great Vowel Shift) explain dzisiejszą ortografię.",
"Probable origin of 'OK' is from 'oll korrect' — żart z XIX wieku.",
"Learn collocations rather than pojedyncze słowa to brzmieć naturalniej.",
"Prefixes like 'anti-', 'pro-' pomagają tworzyć antonimy i przeciwstawne terminy.",
"English is lingua franca w wielu dziedzinach: nauka, biznes, internet.",
"False friends: 'sensible' (EN) = 'rozsądny', nie 'sensowny' w polskim sensie.",
"Suffix '-ess' tworzył feminines (actress) — w nowoczesnym usage często omitted.",
"Loanwords z jidysz i innych: 'schlep', 'klutz' in informal US English.",
"Stress and rhythm praktykuj z nagraniami native speakerów.",
"English has wiele slangu i rejestrów — adaptuj język do sytuacji.",
"Compound adjectives mogą być hyphenated when used before noun.",
"Suffix '-ize' and '-ise' różnią się regionalnie (US vs UK spelling conventions).",
"False friends: 'comprehensive' ≠ 'komprehensywny' w sensie dosłownym — oznacza szczegółowy, wyczerpujący.",
"Word order in questions with auxiliary verbs: 'Have you seen it?'",
"Inflectional endings: -s (3rd person singular), -ed (past), -ing (gerund/participle).",
]

# small extras to vary phrasing
extras = [
    "This often surprises learners.",
    "You can see it in modern vocabulary.",
    "Writers and speakers use it frequently.",
    "It appears in many idioms.",
    "It reflects the language's long history.",
    "It often causes spelling mistakes.",
    "It is a fun thing to notice in texts.",
    "Teachers often highlight this in lessons.",
    "It helps explain seemingly irregular spelling.",
    "It's useful for exam vocabulary."
]

def generate_365_english_facts():
    facts = []
    for s in short_facts_base:
        # ensure the base facts already are full messages
        facts.append(f"{s}.")
    i = 0
    # generate until 365 unique items
    while len(facts) < 365:
        starter = starters[i % len(starters)]
        topic = english_topics[i % len(english_topics)]
        base = short_facts_base[i % len(short_facts_base)]
        extra = extras[i % len(extras)]
        if i % 4 == 0:
            fact = f"{starter}: In {topic}, {base.lower()} {extra}"
        elif i % 4 == 1:
            fact = f"{starter}! {base} It relates to {topic}."
        elif i % 4 == 2:
            fact = f"{starter} — {base} This is a classic {topic} example."
        else:
            fact = f"{starter}: {base} {extra}"
        # clean
        fact = fact.strip()
        if not fact.endswith("."):
            fact += "."
        if fact not in facts:
            facts.append(fact)
        i += 1
        if i > 2000:
            break
    while len(facts) < 288:
        facts.append("Fun fact: keep exploring English every day!")
    return facts

FACTS = generate_365_english_facts()

def get_index_for_day(year, day_of_year):
    rng = random.Random(year)
    perm = list(range(len(FACTS)))
    rng.shuffle(perm)
    idx = perm[(day_of_year - 1) % len(FACTS)]
    return idx

def send_fact(fact):
    if not DISCORD_WEBHOOK_URL:
        print("Set environment variable DISCORD_WEBHOOK_URL (e.g. in GitHub Actions set secret ENGLISH_WEBHOOK).")
        return
    payload = {"content": f"💡 {fact}"}
    headers = {"Content-Type": "application/json"}
    r = requests.post(DISCORD_WEBHOOK_URL, data=json.dumps(payload), headers=headers)
    if r.status_code // 100 == 2:
        print("Sent successfully.")
    else:
        print("Send error:", r.status_code, r.text)

def main():
    arg_day = None
    if len(sys.argv) > 1:
        try:
            arg_day = int(sys.argv[1])
            if not (1 <= arg_day <= 366):
                arg_day = None
        except:
            arg_day = None

    now = datetime.datetime.now()
    year = now.year
    day_of_year = arg_day if arg_day is not None else now.timetuple().tm_yday
    idx = get_index_for_day(year, day_of_year)
    fact = FACTS[idx]
    print(f"Year={year}, day_of_year={day_of_year}, idx={idx}")
    send_fact(fact)

if __name__ == "__main__":
    main()
