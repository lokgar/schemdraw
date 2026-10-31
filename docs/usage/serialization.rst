.. jupyter-execute::
    :hide-code:

    import schemdraw
    import schemdraw.elements as elm


.. _serialize:

Serialization
-------------

Schemdraw Drawings may be serialized to a Python dictionary or to a JSON formatted string.
Output in other formats, such as TOML or YAML, is possible by serializing to a dictionary and using third-party libraries.

Use `schemdraw.to_dict()` to convert a drawing to a dictionary, and `schemdraw.to_json()` to convert to a JSON string. Only built-in elements are currently supported. Image-based and Fritzing part elements are also unsupported.

.. jupyter-execute::

    with schemdraw.Drawing(show=False) as d:
        elm.Resistor().label('100KΩ')
        elm.Capacitor().down().label('0.1μF', loc='bottom')
        elm.Line().left()
        elm.Ground()
        elm.SourceV().up().label('10V')

    j = schemdraw.to_json(d)
    print(j)


Deserialization
===============

To deserialize a Drawing from a dictionary, use `from_dict`.
JSON and TOML may be deserialized using using `from_toml` and `from_json`.

.. jupyter-execute::

    schemdraw.from_json(j)


Data Format
===========

The following sections describe the serialization format for use in hand-writing or generating schematics through other code.
TOML formatted strings are shown here, but the equivalent JSON may also be used.

.. jupyter-execute::

    toml = '''
    elements = [
        {name="Resistor", d="right", label.text="1Ω"},
        {name="Capacitor", d="down", label.text="10μF", label.loc="bottom"},
        {name="Line", d="left"},
        {name="SourceSin", d="up", label.text="10V"}
    ]
    '''
    schemdraw.from_toml(toml)


Elements List
*************

The drawing elements are supplied in an `elements` list, with each element consisting of a table defining the element properties.
In each table, the `name` key is required, with value of one of schemdraw's Element classes, such as `name="Resistor"` or `name="Capacitor"`.
For pictorial elements, preface the name with `pictorial`, such as `name="pictorial.Resistor"`.

.. jupyter-execute::

    toml = '''
    elements = [
        {name="Resistor"},
        {name="Diode"},
        {name="Inductor"}
    ]'''
    schemdraw.from_toml(toml)


Arguments to the element constructor are provided in an `args` key. For example, a polar capacitor:

.. jupyter-execute::

    toml = '''
    elements = [
        {name="Capacitor", args={polar=true}}
    ]'''
    schemdraw.from_toml(toml)

The element's direction is specified with the `d` key, which can have value of `left`, `right`, `up`, or `down`.
Other element methods, such as `at`, `anchor`, `length`, are provided as additional keys to the table.
Methods without an argument, such as `reverse` and `flip`, are given a boolean value.

.. code-block:: text

    {name="Opamp", d="right", flip=true, anchor="in1"}

is equivalent to:

.. code-block:: python

    Opamp().right().anchor('in1').flip()

Provide an `id` key to name the element so it may be referenced later for positioning.

.. jupyter-execute::

    toml = '''
    elements = [
        {id="Q1", name="Opamp"},
        {name="Resistor", at="Q1.out"}
    ]'''
    schemdraw.from_toml(toml)


is equivalent to:

.. code-block:: python

    with Drawing():
        Q1 = Opamp()
        Resistor().at(Q1.out)

Labels
^^^^^^

The `label` key within an element table specifies another table with properties of the label. `label.text` is required, while other parameters typically passed to `Element.label()` may be given as additional keys.

.. jupyter-execute::

    toml = '''
    elements = [
        {name="Resistor", label.text="R1"},
        {name="Resistor", label.text="a", label.loc="right", label.halign="left"}
    ]'''
    schemdraw.from_toml(toml)

Some elements need multiple labels. Use `labels.1.text`, `labels.2.text`, etc. to add multiple labels to the same element.

.. jupyter-execute::

    toml = '''
    elements = [
        {name="Resistor", labels.1.text="100", labels.2.text="R1", labels.2.loc="bottom"}
    ]'''
    schemdraw.from_toml(toml)


Drawing commands
^^^^^^^^^^^^^^^^

Elements named `move`, `moveto`, `push`, and `pop` provide functions to control the drawing cursor position

.. jupyter-execute::

    toml = '''
    elements = [
        {name="Dot", color="red"},
        {name="push"},
        {name="move", dx=3, dy=0},
        {name="Dot", color="blue"},
        {name="pop"},
        {name="Line", d="right", length=0.5}
    ]'''
    schemdraw.from_toml(toml)



Configuration
*************

The top-level `config` key in the TOML or JSON is equivalent to calling `schemdraw.config` with the values in the config table as parameters.

.. code-block:: text

    config = {unit=1, fontsize=10}

is equivalent to

    schemdraw.config(unit=1, fontsize=10)

Another top-level `style` key, set to either string `IEEE` or `IEC`, replaces `schemdraw.style` for switching between IEEE and IEC style elements

.. code-block:: text

    style="IEC"

The `defaults` top-level key allows for setting default parameters on any element class, simiar to setting values in an `Element.defaults` dictionary.
For example, to fill all Diodes,

.. code-block:: text

    defaults = {Diode={fill=true}}

is equivalent to Python

.. code-block:: python

    elm.Diode.defaults[fill] = True


Subdrawings
***********
The `ElementDrawing` class is replaced using the `subdrawings` top-level key in the TOML or JSON.
The value is a table of named drawings, each with an `elements` list following the same format described above.
The subdrawing may then be reused as an element name.

.. jupyter-execute::

    toml = '''
    subdrawings = {d1={elements=[
            {id="R1", name="Resistor"},
            {id="C1", name="Capacitor", d="down"},
            {name="Line", d="left"},
            {name="moveto", to="R1.end"}]}}

    elements = [
        {name="d1"},
        {name="d1"},
        {name="d1"},
        {name="push"},
        {name="Line", length=0.5},
        {name="DotDotDot"},
        {name="d1"},
        {name="pop"},
        {name="move", dy=-3},
        {name="Line", d="right", length=0.5},
        {name="DotDotDot"}
    ]
    '''
    schemdraw.from_toml(toml)


Examples
********

Some examples from other parts of this documentation rewritten as TOML input.

.. jupyter-execute::

    toml = '''
    config = {unit=2}
    elements = [
        {id="R1", name="Resistor", d="down", label={text="20Ω"}},
        {id="V1", name="SourceV", d="down", reverse=true, label.text="120V"},
        {name="Line", d="right", length=3, dot=true},
        {name="Line", at="R1.start", length=3, d="right", dot=true},
        {name="SourceV", d="down", reverse=true, label.text="60V"},
        {name="Resistor", label={text="5Ω"}},
        {name="Line", d="right", length=3, dot=true},
        {name="SourceI", d="up", label.text="36A"},
        {name="Resistor", label.text="36A", dot=true},
        {name="Line", d="left", length=3, hold=true},
        {name="Line", d="right", length=3, dot=true},
        {id="R6", name="Resistor", toy="V1.end", label.text="6Ω"},
        {name="Line", d="left", length=3, hold=true},
        {name="Resistor", d="right", at="R6.start", label.text="1.6Ω"},
        {name="Dot", args.open=true, label.text="a", label.loc="right"},
        {name="Line", d="right", at="R6.end", label.text="b", label.loc="right"}
    ]
    '''
    schemdraw.from_toml(toml)

|

.. jupyter-execute::

    toml = '''
    elements = [
        {id="op", name="Opamp", args={leads=true}},
        {name="Line", d="down", length="unit/4", at="op.in2"},
        {name="Ground", args={lead=false}},
        {name="Dot", at="op.in1"},
        {id="Rin", name="Resistor", at="op.in1", d="left", labels.1.text="$R_{in}$", labels.1.loc="bottom", labels.2.text="$v_{in}$", labels.2.loc="left"},
        {name="Line", d="up", length="unit/2", at="op.in1"},
        {name="Resistor", tox="op.out", label.text="$R_f$"},
        {name="Line", toy="op.out", dot=true},
        {name="Line", d="right", length="unit/4", at="op.out", label.text="$v_{o}$", label.loc="right"}
    ]
    '''
    schemdraw.from_toml(toml)


The `Container` element contains another list of elements to include in the container.

.. jupyter-execute::

    toml = r'''
    config = {unit=1}

    elements = [
        {name="Start", label.text="Start"},
        {name="Arrow", d="down", length=1.5},
        {name="Container", color="red", elements=[
            {name="Box", label.text="Step 1", drop="E"},
            {name="Arrow", d="right"},
            {name="Box", label.text="Step 2"}
        ], label.text="Subprocess", label.loc="N", label.halign="center"},
        {name="Arrow", d="right", length=1.5},
        {name="Start", anchor="W", label.text="End"}
        ]
    '''
    schemdraw.from_toml(toml)

Integrated circuit pins:

.. jupyter-execute::

    toml = r'''
    elements = [
        {name="Ic", pins=[
            {name=">", pin="1", side="left"},
            {name="K", pin="16", side="left"},
            {name="J", pin="4", side="left"},
            {name="$\\overline{Q}$", pin="14", side="right"},
            {name="Q", pin="15", side="right"}
            ], args={pinspacing=1, edgepadW=0.5}}
    ]
    '''
    schemdraw.from_toml(toml)

The same diagram read from JSON format:

.. jupyter-execute::

    j = r'''{
    "elements": [
        {
        "name": "Ic",
        "pins": [
            {
            "name": ">",
            "pin": "1",
            "side": "left"
            },
            {
            "name": "K",
            "pin": "16",
            "side": "left"
            },
            {
            "name": "J",
            "pin": "4",
            "side": "left"
            },
            {
            "name": "$\\overline{Q}$",
            "pin": "14",
            "side": "right"
            },
            {
            "name": "Q",
            "pin": "15",
            "side": "right"
            }
        ],
        "args": {
            "pinspacing": 1,
            "edgepadW": 0.5
        }
        }
    ]
    }'''
    schemdraw.from_json(j)
