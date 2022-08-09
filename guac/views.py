import libvirt

from base64 import urlsafe_b64decode
from django.shortcuts import render
from xml.etree import ElementTree as ET


def index(request, task_id, session_data):
    dsn = "qemu:///system"
    conn = libvirt.open(dsn)
    recording_name = f"{task_id}_recording"
    if conn:
        try:
            session_id, label = urlsafe_b64decode(session_data).decode("utf8").split("|")
            dom = conn.lookupByName(label)
            if dom:
                state = dom.state(flags=0)
        except Exception as e:
            return render(request, "guac/error.html", {"error_msg": e})

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
                    "recording_name": recording_name,
                },
            )
        else:
            return render(request, "guac/wait.html")


def playback(request, task_id):
    playback_url = f"{task_id}_recording"

    if playback_url:
        return render(
            request,
            "guac/playback.html",
            {
                "playback_url": playback_url,
            },
        )
    else:
        return render(
            request, "guac/error.html", {"error_msg": f"Does not exist: {playback_url}"}
        )
