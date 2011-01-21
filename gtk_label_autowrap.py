#
# Copyright (C) 2004, 2007 Red Hat, Inc.
# Authors:
# Thomas Woerner <twoerner@redhat.com>
# Florian Festi <ffesti@redhat.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

from gi.repository import Gtk
from pango import SCALE

### set autowrapping for all labels in this widget tree
def set_autowrap(widget):
    return #TODO: currently doesn't work with GTK/pygi, and it is not really
           # making a visible improvement anyway
    if isinstance(widget, Gtk.Container):
        children = widget.get_children()
        for i in xrange(len(children)):
            set_autowrap(children[i])
    elif isinstance(widget, Gtk.Label) and widget.get_line_wrap():
        widget.connect_after("size-allocate", label_size_allocate)
        widget.set_property("xalign", 0)
        widget.set_property("yalign", 0)

### set wrap width to the Pango.Layout of the labels ###
def label_size_allocate(widget, allocation):
    layout = widget.get_layout()

    lw_old, lh_old = layout.get_pixel_size()

    # fixed width labels
    if lw_old == allocation.width:
        return

    layout.set_width(allocation.width * SCALE)
    lw, lh = layout.get_pixel_size()

    if lh_old != lh:
        widget.set_size_request(-1, lh)

##############################################################################

if __name__ == "__main__":
    window = Gtk.Window(Gtk.WindowType.TOPLEVEL)
    window.connect("delete_event", Gtk.main_quit)

    label = Gtk.Label(label="When you invoke GCC, it normally does preprocessing, compilation, assembly and linking.")
    label.set_line_wrap(True)
    label.set_use_markup(True)
    label.set_property("xalign", 1)
    label.set_property("yalign", 1)

    hbox = Gtk.HBox()
    hbox.pack_start(label)
#    window.add(label)
    window.add(hbox)
    set_autowrap(window)

    window.set_resizable(True)
    window.show_all()
    Gtk.main()
