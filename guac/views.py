import libvirt

from django.shortcuts import render
from xml.etree import ElementTree as ET


def index(request, label, session_id):
    dsn = "qemu:///system"
    conn = libvirt.open(dsn)
    if conn:
        dom = conn.lookupByName(label)
        if dom:
            state = dom.state(flags=0)

    if state:
        if state[0] == 1:
            status = "RUNNING"
            vmXml = dom.XMLDesc(0)
            root = ET.fromstring(vmXml)
            graphics = root.find("./devices/graphics")
            vncport = graphics.get("port")
            return render(
                request,
                "guac/index.html",
                {
                    "vncport": vncport,
                    "session_id": session_id,
                },
            )
        else:
            return render(request, "guac/wait.html")
