"""
Views.
"""

from django.shortcuts import render

BASE_PAIRING = {
    'A': 'T',
    'C': 'G',
    'G': 'C',
    'T': 'A',
}

TRANSCRIPTION_PAIRING = {
    'A': 'U',
    'T': 'A',
    'G': 'C',
    'C': 'G'
}

TRANSLATION_MAPPING = {
    'UUU': 'F', 'UUC': 'F',
    'UUA': 'L', 'UUG': 'L', 'CUU': 'L', 'CUC': 'L', 'CUA': 'L',
    'CUG': 'L', 'AUU': 'I', 'AUC': 'I',
    'AUG': 'M',
    'GUU': 'V', 'GUC': 'V', 'GUA': 'V', 'GUG': 'V',
    'UCU': 'S', 'UCC': 'S', 'UCA': 'S', 'UCG': 'S',
    'CCU': 'P', 'CCC': 'P', 'CCA': 'P', 'CCG': 'P',
    'ACU': 'T', 'ACC': 'T', 'ACA': 'T', 'ACG': 'T',
    'GCU': 'A', 'GCC': 'A', 'GCA': 'A', 'GCG': 'A',
    'UAU': 'Y', 'UAC': 'Y',
    'UAA': 'X', 'UAG': 'X',
    'CAU': 'H', 'CAC': 'H',
    'CAA': 'Q', 'CAG': 'Q',
    'AAU': 'N', 'AAC': 'N',
    'AAA': 'K', 'AAG': 'K',
    'UGA': 'X',
    'UGG': 'W',
    'CGU': 'R', 'CGC': 'R', 'CGA': 'R', 'CGG': 'R',
    'GGU': 'N', 'GGC': 'R', 'GGA': 'G', 'GGG': 'G',
}

def home(request):
    context = {}

    def split(str, num):
        return [ str[start:start+num] for start in range(0, len(str), num) ]

    # Check whether this request includes a query string to translate.
    query_string = request.GET.get('query', '').strip()
    if len(query_string):
        query_string = query_string.upper()
        reverse_complement = ''
        transcribed = ''
        for base in query_string:
            if base in BASE_PAIRING:
                reverse_complement += BASE_PAIRING[base]
                transcribed += TRANSCRIPTION_PAIRING[base]
            else:
                context['error'] = '{0} is not a valid nucleobase.'.format(base)
                return render(request, 'home.html', context)

        codons = split(transcribed, 3)
        amino_acids = [TRANSLATION_MAPPING.get(x, "?") for x in codons]
        translation = "." + "..".join(amino_acids) + "."

        context['query_string'] = query_string
        context['reverse_complement'] = reverse_complement
        context['transcribed'] = transcribed
        context['translation'] = translation

    return render(request, 'home.html', context)
