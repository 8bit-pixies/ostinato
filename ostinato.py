"""
Ostinato
========

A simple ostinator generator.

"""

from abjad import *
import re

def make_chord(num, index0=True):
    """make chord from scale number"""
    if index0==False:
        num = (num+7) % 8
    return (num, (num+2) % 7, (num+4) % 7)


def find_key(lystring):
    """tries to find the key in the lilypond file using regex (since I can't
    figure out the appropriate way using abjad API)"""
    try:
        m = re.search(r'(\\key\s+[a-g]\s+\\m(?:aj|in)or)', lystring)
        info = m.group(0).split()        
        return KeySignature(info[-2], info[-1][1:])
    except:
        return KeySignature('c', 'major')
        
def find_time(lystring):
    """tries to find the time signature in the lilypond file using regex(since
    I can't figure out the appropriate way using abjad API)"""
    try:
        m = re.search(r'\\time\s+(\d+/\d+)', lystring)
        info = m.group(1).split("/")
        return TimeSignature((int(info[0]), int(info[1])))
    except:
        return TimeSignature((4,4))

def get_score(lystring):
    """lystring: lilypond string"""
    parser = lilypondparsertools.LilyPondParser()
    parsed = Staff([parser(lystring)])
    key_signature = find_key(lystring)
    attach(key_signature, parsed)
    time_signature = find_time(lystring)
    attach(time_signature, parsed)
    return parsed

def get_key_mapping(keysig):
    key_mapping = {}
    cmajor = [0, 2, 4, 5, 7, 9, 11]    
    mode_name = keysig.mode.mode_name
    pitch = keysig.tonic.pitch_class_number

    if mode_name == 'major':
        keymap = cmajor 
        note = Note('c') # note.written_pitch.pitch_class_number
    else:
        keymap = cmajor[-2:] + cmajor[:-2] # this is a minor   
        note = Note('a') # note.written_pitch.pitch_class_number
        
    transpose_delta = pitch - note.written_pitch.pitch_class_number    
    
    scale = Staff(scoretools.make_notes(map(lambda x: x + transpose_delta, keymap), Duration(1,8)))
    
    for i, note in enumerate(iterate(scale).by_class(Note)):
        key_mapping[note.written_pitch.pitch_class_name] = i
    return key_mapping
    
def ostinato(lystring):
    def create_chord(chordmap, rev_score_keymap, dur):
        chord = Chord("<%s>" % ' '.join([rev_score_keymap[x] for x in chordmap]))
        chord.written_duration = dur
        return chord
        
    # define the chord mappings   
    CHORD_MAP = {}
    for x in range(7):
        CHORD_MAP[x] = sorted([x, (x+2)%7, (x+4)%7])
        
    # get the score
    music_score = get_score(lystring)
    music_score_lh = music_score[0] # force into container
    
    score_keymap = get_key_mapping(inspect_(get_score(lystring)).get_indicator(KeySignature))
    rev_score_keymap = dict(zip(score_keymap.values(), score_keymap.keys()))
    
    # remap every single note to the mapping provided/get the strong note, and to the right chord.
    generator = iterate(music_score_lh).by_class(Note)
    for i, x in enumerate(generator):
        note_key = score_keymap[x.written_pitch.pitch_class_name]
        #print note_key
        
        # must be a better way... this assumes, I IV V I pattern
        if note_key in CHORD_MAP[0]:
            chord = create_chord(CHORD_MAP[0], rev_score_keymap, x.written_duration)
            music_score_lh[i] = chord
        elif note_key in CHORD_MAP[3]:
            chord = create_chord(CHORD_MAP[3], rev_score_keymap, x.written_duration)
            music_score_lh[i] = chord
        elif note_key in CHORD_MAP[4]:
            chord = create_chord(CHORD_MAP[4], rev_score_keymap, x.written_duration)
            music_score_lh[i] = chord
        elif note_key == 2:
            chord = create_chord(CHORD_MAP[4], rev_score_keymap, x.written_duration)
            music_score_lh[i] = chord

    ms_lh = Staff([music_score_lh])
    clef = Clef('bass')
    attach(clef, ms_lh)
    
    piano_staff = scoretools.StaffGroup([], context_name='PianoStaff')
    piano_staff.append(get_score(lystring))
    piano_staff.append(ms_lh)
    return piano_staff

if __name__ == "__main__":
    mary_had_a_little_lamb = r"""  \relative c'
    {
    
    \time 4/4
    e d c d
    e e e2
    d4 d d2
    e4 g g2
    e4 d c d
    e e e e
    d d e d
    c1
    }
    """
    
    print format(ostinato(mary_had_a_little_lamb))
