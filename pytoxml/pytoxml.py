from types import (DictType, StringTypes, IntType, FloatType,
                   TupleType, ListType)

try:
    from lxml import etree
except ImportError:
    try:
        import xml.etree.cElementTree as etree
        print "Using cElemenTree"
    except ImportError:
        try:
            import xml.etree.ElementTree as etree
            print "Using ElemenTree"
        except ImportError:
            print "Failed to import ElementTree"
            raise


class PyToXml(object):
    """Class which allows you convert a deeply nested python structure
    into an XML representation."""
    def __init__(self, root_name, structure,
                 encoding="UTF-8", xml_declaration=False):
        self.root = etree.Element(root_name)
        self.root_name = root_name
        self.structure = structure
        self.encoding = encoding
        self.xml_declaration = xml_declaration
        if xml_declaration and not etree.__name__ == "lxml.etree":
            raise TypeError("Not using lxml, can't use xml_declaration")

    def pluralisation(self, plural):
        """Returns a string that is suitable for elements of a
        list. Intended to be overridden for more complex pluralisation
        logic."""
        return "item"

    def traverse(self, structure, document, name):
        """Loop over the structure, convert to an etree style document
        and apply to document. The argument name is the element name
        of the parent."""
        if isinstance(structure, StringTypes):
            document.text = structure

        elif isinstance(structure, (ListType, TupleType)):
            for value in structure:
                sub = etree.SubElement(document, self.pluralisation(name))
                self.traverse(value, sub, name)

        elif isinstance(structure, DictType):
            for key, value in structure.iteritems():
                sub = etree.SubElement(document, key)
                self.traverse(value, sub, key)

        elif type(structure) == bool:
            document.text = str(structure).lower()

        elif isinstance(structure, (IntType, FloatType)):
            document.text = str(structure)

        else:
            raise TypeError("Can't serialise %s" % type(structure))

    def encode(self):
        """Encode the structure passed into the constructor as
        XML. This method must be called before this object is output
        as a string."""
        self.traverse(self.structure, self.root, self.root_name)

        return self

    def __str__(self):
        """Output the XML."""
        if self.xml_declaration:
            return etree.tostring(self.root,
                                  encoding=self.encoding,
                                  xml_declaration=self.xml_declaration)
        else:
            return etree.tostring(self.root,
                                  encoding=self.encoding)
