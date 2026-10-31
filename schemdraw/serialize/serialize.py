''' Serialize a Drawing to dictionary or JSON

    TOML is read-only since tomllib doesn't have write ability as of
    Python 3.15. The to_dict method converts a Drawing to dictionary
    that coulud be serialized to TOML using a third-party dependency.
'''
from typing import TYPE_CHECKING, Type, Any
from dataclasses import asdict
import json

from .. import elements as elm
from .. import flow

if TYPE_CHECKING:
    from ..schemdraw import Drawing


def element_to_dict(e: elm.Element) -> tuple[dict, dict]:
    ''' Convert one element to a dictionary '''
    subdrawings: dict[str, dict] = {}
    cfg: dict[str, Any] = {'name': e.__class__.__name__}


    params = e._userparams.copy()
    for key in ['anchor', 'color', 'drop', 'fill', 'theta', 'shift', 'linestyle',
                'linewidth', 'scale', 'scalex', 'scaley', 'zorder',
                'length', 'drop', 'at'
            ]:
        if (value := params.pop(key, None)):
            cfg[key] = value

    # Hacks to fix specific elements
    if isinstance(e, flow.Start):
        cfg['name'] = 'Start'
    if isinstance(e, elm.Ic) and not e.fixed_pins:
    # Format IcPins
        params.pop('pins', None)  # Remove from user config, and read from .pins attribute
        pins = []
        for pin in e.pins['L'] + e.pins['R'] + e.pins['T'] + e.pins['B']:
            pins.append({k:v for k, v in asdict(pin).items() if v is not None})
            if 'pinlblsize' in pins[-1]:
                pins[-1]['lblsize'] = pins[-1].pop('pinlblsize', None)
        cfg['pins'] = pins
        if e.usersides:
            cfg['sides'] = {}
            for name, side in e.usersides.items():
                cfg['sides'][name] = {k:v for k, v in asdict(side).items() if v is not None}
    if isinstance(e, elm.ElementDrawing):
        subname = f'd{len(subdrawings)}'
        subdrawings[subname] = to_dict(e.drawing)
        cfg['name'] = subname
    if isinstance(e, elm.Container):
        params.pop('drawing', None)
        params.pop('at', None)
        cfg.pop('at', None)
        cfg['elements'] = []
        for cont_elm in e.elements:
            ecfg, subs = element_to_dict(cont_elm)
            cfg['elements'].append(ecfg)
            subdrawings.update(subs)

    params.pop('d', None)  # 'd' will be replaced by 'theta' from drawing placement
    if params:
        # Anything remaining parameters go into Element instantiation
        cfg['args'] = params
    if isinstance(e, (elm.Coax, elm.Triax)) and 'length' in e._userparams:
        # Coax/Triax have a `length` parameter separate from length method
        cfg['args']['length'] = e._userparams['length']

    # Labels
    for i, label in enumerate(e._userlabels):
        lblcfg = {name: value for name, value in asdict(label).items() if value is not None}
        lblcfg['text'] = lblcfg.pop('label', '')
        cfg.setdefault('labels', {})
        cfg['labels'][str(i)] = lblcfg

    if not isinstance(e, elm.Container):
        cfg.setdefault('at', e.placed_cursor['xy'])
    cfg.setdefault('theta', e.placed_cursor['theta'])
    return cfg, subdrawings


def to_dict(d: 'Drawing') -> dict:
    ''' Convert a drawing to a dictionary that can be serialized to JSON '''
    elements = []
    subdrawings: dict[str, dict] = {}
    for e in d.elements:
        if not e.elmparams.get('in_container'):
            elmcfg, subdwgs = element_to_dict(e)
            elements.append(elmcfg)
            subdrawings.update(subdwgs)

    config = {}
    for cfgitem in ['unit', 'inches_per_unit', 'fontsize', 'font', 'color',
                    'lw', 'ls', 'fill', 'bgcolor', 'margin', 'mathfont']:
        if (value := d.dwgparams.get(cfgitem)):
            config[cfgitem] = value

    out = {'elements': elements, 'config': config}
    if subdrawings:
        out['subdrawings'] = subdrawings
    return out


def to_json(d: 'Drawing') -> str:
    ''' Serialize the Drawing to JSON '''
    return json.dumps(to_dict(d))

