opsConfigFieldsDocMap = [
{
    "key"   : "PlaMode",
    "scope" : ["pla","plafull","dd","tr","trfull"],
    "doc"   : F("""\
                Description
                    This field configures the software to a specific operational mode.

                Supported values
                * pl
                * dd
                * tr

                This is a mandatory field.
                Example
                    PlaMode = dd""")
},
{
    "key"   : "PlaMode",
    "scope" : ["player","playerfull","doordarshan","transcoder","transcoderfull"],
    "doc"   : F("""\
                Description
                    This field configures the software to a specific operational mode.

                Supported values
                * pl
                * dd
                * tr

                This is a mandatory field.
                Example
                    PlaMode = dd""")
},
{
    "key"   : "EnableOpsConfig",
    "scope" : ["pla","plafull","dd","tr","trfull"],
    "doc"   : F("""\
                Description
                    The configuration enables or disables usage of CMS
                    software for generation Cloudport Player configurations.

                Supported values
                * true
                * false

                This is a mandatory field.
                When in doubt, configure to true.

                Example
                    EnableOpsConfig = true""")
},
{
    "key"   : "EnableOpsConfig",
    "scope" : ["player","playerfull","doordarshan","transcoder","transcoderfull"],
    "doc"   : F("""\
                Description
                    The enables or disables usage of CMS
                    software for generation Cloudport Player configurations.

                Supported values
                * true
                * false

                This is a mandatory field.
                When in doubt, configure to true.

                Example
                    EnableOpsConfig = true""")
},
{
    "key"   : "BlipFeedResolution",
    "scope" : ["pla","plafull"],
    "doc"   : F("""\
                Description
                    Configuration for resolution and frame rate of Blip in Player.
                    This field is used to create filenames of IMT and DVB subtitle
                    files.

                Format
                    <width>x<height><scantype><framerate>

                    Please note the 'x' between width and height.

                    where,
                        * width       : pixel width of video frames
                        * height      : pixel height of video frames
                        * scantype    : video frame scan type.
                                        Supported types are i(interlaced) and p(progressive)
                        * framerate   : Video frames per second

                Supported values
                * 720x576i50        (DVB,IMT)
                * 720x480i59.94     (DVB)
                * 1920x1080i50      (DVB)
                * 1920x1080i59.94   (DVB)

                This field is mandatory if IMT or DVB subtitle file playback
                feature is needed.

                Example
                    BlipFeedResolution = 720x576i50""")
}
]