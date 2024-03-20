import xml.etree.ElementTree as ET


def rgb_to_hex(r, g, b):
    return '{:02x}{:02x}{:02x}'.format(r, g, b)


def convert_xml(xml_string):
	root = ET.fromstring(xml_string)
	new_root = ET.Element(root.tag)

	for child in root:
		r = child.find('R')
		g = child.find('G')
		b = child.find('B')

		if r is not None and g is not None and b is not None:
			r_value = int(r.get('Value'))
			g_value = int(g.get('Value'))
			b_value = int(b.get('Value'))
			hex_value = rgb_to_hex(r_value, g_value, b_value)
			new_element = ET.Element(child.tag, Value='#' + hex_value)
			new_root.append(new_element)
		else:
			newChild = child
			# trim newchild 
			new_root.append(newChild)

	new_xml_string = ET.tostring(new_root, encoding='unicode')
	formatted_xml_string = new_xml_string.replace('><', '>\n<')
	return formatted_xml_string


def main():
	xml_string = """
	<SkinManager>
		<ControlForeground>
			<R Value="238" />
			<G Value="238" />
			<B Value="238" />
			<Alpha Value="255" />
		</ControlForeground>
		<TextDisabled>
			<R Value="140" />
			<G Value="140" />
			<B Value="140" />
			<Alpha Value="255" />
		</TextDisabled>
		<ControlDisabled>
			<R Value="160" />
			<G Value="160" />
			<B Value="160" />
			<Alpha Value="255" />
		</ControlDisabled>
		<MeterBackground>
			<R Value="40" />
			<G Value="40" />
			<B Value="40" />
			<Alpha Value="255" />
		</MeterBackground>
		<SurfaceHighlight>
			<R Value="120" />
			<G Value="120" />
			<B Value="120" />
			<Alpha Value="255" />
		</SurfaceHighlight>
		<SurfaceArea>
			<R Value="65" />
			<G Value="65" />
			<B Value="65" />
			<Alpha Value="255" />
		</SurfaceArea>
		<Desktop>
			<R Value="80" />
			<G Value="80" />
			<B Value="80" />
			<Alpha Value="255" />
		</Desktop>
		<ViewCheckControlEnabledOn>
			<R Value="26" />
			<G Value="164" />
			<B Value="230" />
			<Alpha Value="255" />
		</ViewCheckControlEnabledOn>
		<ScrollbarInnerHandle>
			<R Value="170" />
			<G Value="170" />
			<B Value="170" />
			<Alpha Value="255" />
		</ScrollbarInnerHandle>
		<ScrollbarInnerTrack>
			<R Value="0" />
			<G Value="0" />
			<B Value="0" />
			<Alpha Value="255" />
		</ScrollbarInnerTrack>
		<ScrollbarOuterHandle>
			<R Value="170" />
			<G Value="170" />
			<B Value="170" />
			<Alpha Value="255" />
		</ScrollbarOuterHandle>
		<ScrollbarOuterTrack>
			<R Value="0" />
			<G Value="0" />
			<B Value="0" />
			<Alpha Value="255" />
		</ScrollbarOuterTrack>
		<ScrollbarLCDHandle>
			<R Value="160" />
			<G Value="160" />
			<B Value="160" />
			<Alpha Value="255" />
		</ScrollbarLCDHandle>
		<ScrollbarLCDTrack>
			<R Value="160" />
			<G Value="160" />
			<B Value="160" />
			<Alpha Value="255" />
		</ScrollbarLCDTrack>
		<DetailViewBackground>
			<R Value="120" />
			<G Value="120" />
			<B Value="120" />
			<Alpha Value="255" />
		</DetailViewBackground>
		<PreferencesTab>
			<R Value="95" />
			<G Value="95" />
			<B Value="95" />
			<Alpha Value="255" />
		</PreferencesTab>
		<SelectionFrame>
			<R Value="0" />
			<G Value="0" />
			<B Value="0" />
			<Alpha Value="255" />
		</SelectionFrame>
		<ControlBackground>
			<R Value="80" />
			<G Value="80" />
			<B Value="80" />
			<Alpha Value="255" />
		</ControlBackground>
		<ControlFillHandle>
			<R Value="120" />
			<G Value="120" />
			<B Value="120" />
			<Alpha Value="255" />
		</ControlFillHandle>
		<ChosenDefault>
			<R Value="45" />
			<G Value="187" />
			<B Value="255" />
			<Alpha Value="255" />
		</ChosenDefault>
		<ChosenRecord>
			<R Value="254" />
			<G Value="44" />
			<B Value="44" />
			<Alpha Value="250" />
		</ChosenRecord>
		<ChosenPreListen>
			<R Value="67" />
			<G Value="145" />
			<B Value="230" />
			<Alpha Value="255" />
		</ChosenPreListen>
		<ImplicitArm>
			<R Value="0" />
			<G Value="159" />
			<B Value="244" />
			<Alpha Value="255" />
		</ImplicitArm>
		<RangeDefault>
			<R Value="109" />
			<G Value="215" />
			<B Value="255" />
			<Alpha Value="255" />
		</RangeDefault>
		<RangeDisabled>
			<R Value="160" />
			<G Value="160" />
			<B Value="160" />
			<Alpha Value="255" />
		</RangeDisabled>
		<RangeDisabledOff>
			<R Value="75" />
			<G Value="75" />
			<B Value="75" />
			<Alpha Value="255" />
		</RangeDisabledOff>
		<LearnMidi>
			<R Value="101" />
			<G Value="112" />
			<B Value="245" />
			<Alpha Value="255" />
		</LearnMidi>
		<LearnKey>
			<R Value="255" />
			<G Value="100" />
			<B Value="0" />
			<Alpha Value="255" />
		</LearnKey>
		<LearnMacro>
			<R Value="0" />
			<G Value="218" />
			<B Value="72" />
			<Alpha Value="255" />
		</LearnMacro>
		<RangeEditField>
			<R Value="66" />
			<G Value="105" />
			<B Value="120" />
			<Alpha Value="255" />
		</RangeEditField>
		<RangeEditField2>
			<R Value="147" />
			<G Value="86" />
			<B Value="84" />
			<Alpha Value="255" />
		</RangeEditField2>
		<BipolReset>
			<R Value="109" />
			<G Value="215" />
			<B Value="255" />
			<Alpha Value="255" />
		</BipolReset>
		<ChosenAlternative>
			<R Value="185" />
			<G Value="252" />
			<B Value="255" />
			<Alpha Value="255" />
		</ChosenAlternative>
		<ChosenAlert>
			<R Value="255" />
			<G Value="100" />
			<B Value="70" />
			<Alpha Value="255" />
		</ChosenAlert>
		<ChosenPlay>
			<R Value="0" />
			<G Value="255" />
			<B Value="129" />
			<Alpha Value="255" />
		</ChosenPlay>
		<Clip1>
			<R Value="139" />
			<G Value="121" />
			<B Value="54" />
			<Alpha Value="255" />
		</Clip1>
		<Clip2>
			<R Value="153" />
			<G Value="149" />
			<B Value="101" />
			<Alpha Value="255" />
		</Clip2>
		<Clip3>
			<R Value="184" />
			<G Value="206" />
			<B Value="147" />
			<Alpha Value="255" />
		</Clip3>
		<Clip4>
			<R Value="175" />
			<G Value="185" />
			<B Value="91" />
			<Alpha Value="255" />
		</Clip4>
		<Clip5>
			<R Value="82" />
			<G Value="186" />
			<B Value="70" />
			<Alpha Value="255" />
		</Clip5>
		<Clip6>
			<R Value="129" />
			<G Value="210" />
			<B Value="76" />
			<Alpha Value="255" />
		</Clip6>
		<Clip7>
			<R Value="107" />
			<G Value="170" />
			<B Value="206" />
			<Alpha Value="255" />
		</Clip7>
		<Clip8>
			<R Value="72" />
			<G Value="129" />
			<B Value="170" />
			<Alpha Value="255" />
		</Clip8>
		<Clip9>
			<R Value="149" />
			<G Value="78" />
			<B Value="178" />
			<Alpha Value="255" />
		</Clip9>
		<Clip10>
			<R Value="255" />
			<G Value="95" />
			<B Value="128" />
			<Alpha Value="255" />
		</Clip10>
		<Clip11>
			<R Value="220" />
			<G Value="72" />
			<B Value="72" />
			<Alpha Value="255" />
		</Clip11>
		<Clip12>
			<R Value="214" />
			<G Value="107" />
			<B Value="24" />
			<Alpha Value="255" />
		</Clip12>
		<Clip13>
			<R Value="224" />
			<G Value="170" />
			<B Value="42" />
			<Alpha Value="255" />
		</Clip13>
		<Clip14>
			<R Value="255" />
			<G Value="236" />
			<B Value="117" />
			<Alpha Value="255" />
		</Clip14>
		<Clip15>
			<R Value="231" />
			<G Value="230" />
			<B Value="230" />
			<Alpha Value="255" />
		</Clip15>
		<Clip16>
			<R Value="160" />
			<G Value="160" />
			<B Value="160" />
			<Alpha Value="255" />
		</Clip16>
		<ClipText>
			<R Value="0" />
			<G Value="0" />
			<B Value="0" />
			<Alpha Value="255" />
		</ClipText>
		<ClipBorder>
			<R Value="255" />
			<G Value="255" />
			<B Value="255" />
			<Alpha Value="255" />
		</ClipBorder>
		<SelectionBackground>
			<R Value="199" />
			<G Value="237" />
			<B Value="255" />
			<Alpha Value="255" />
		</SelectionBackground>
		<StandbySelectionBackground>
			<R Value="138" />
			<G Value="158" />
			<B Value="167" />
			<Alpha Value="255" />
		</StandbySelectionBackground>
		<SelectionForeground>
			<R Value="20" />
			<G Value="20" />
			<B Value="20" />
			<Alpha Value="255" />
		</SelectionForeground>
		<StandbySelectionForeground>
			<R Value="20" />
			<G Value="20" />
			<B Value="20" />
			<Alpha Value="255" />
		</StandbySelectionForeground>
		<SurfaceBackground>
			<R Value="95" />
			<G Value="95" />
			<B Value="95" />
			<Alpha Value="255" />
		</SurfaceBackground>
		<AutomationColor>
			<R Value="249" />
			<G Value="62" />
			<B Value="62" />
			<Alpha Value="255" />
		</AutomationColor>
		<AutomationGrid>
			<R Value="0" />
			<G Value="0" />
			<B Value="0" />
			<Alpha Value="255" />
		</AutomationGrid>
		<LoopColor>
			<R Value="20" />
			<G Value="20" />
			<B Value="20" />
			<Alpha Value="255" />
		</LoopColor>
		<OffGridLoopColor>
			<R Value="20" />
			<G Value="20" />
			<B Value="20" />
			<Alpha Value="95" />
		</OffGridLoopColor>
		<ArrangementRulerMarkings>
			<R Value="180" />
			<G Value="180" />
			<B Value="180" />
			<Alpha Value="255" />
		</ArrangementRulerMarkings>
		<DetailViewRulerMarkings>
			<R Value="238" />
			<G Value="238" />
			<B Value="238" />
			<Alpha Value="255" />
		</DetailViewRulerMarkings>
		<ShadowDark>
			<R Value="0" />
			<G Value="0" />
			<B Value="0" />
			<Alpha Value="139" />
		</ShadowDark>
		<ShadowLight>
			<R Value="95" />
			<G Value="95" />
			<B Value="95" />
			<Alpha Value="200" />
		</ShadowLight>
		<DisplayBackground>
			<R Value="65" />
			<G Value="65" />
			<B Value="65" />
			<Alpha Value="255" />
		</DisplayBackground>
		<AbletonColor>
			<R Value="14" />
			<G Value="160" />
			<B Value="216" />
			<Alpha Value="255" />
		</AbletonColor>
		<WaveformColor>
			<R Value="20" />
			<G Value="20" />
			<B Value="20" />
			<Alpha Value="220" />
		</WaveformColor>
		<VelocityColor>
			<R Value="255" />
			<G Value="88" />
			<B Value="76" />
			<Alpha Value="255" />
		</VelocityColor>
		<Alert>
			<R Value="255" />
			<G Value="56" />
			<B Value="21" />
			<Alpha Value="255" />
		</Alert>
		<ControlOnForeground>
			<R Value="20" />
			<G Value="20" />
			<B Value="20" />
			<Alpha Value="255" />
		</ControlOnForeground>
		<ControlOffForeground>
			<R Value="238" />
			<G Value="238" />
			<B Value="238" />
			<Alpha Value="255" />
		</ControlOffForeground>
		<ControlOnDisabledForeground>
			<R Value="65" />
			<G Value="65" />
			<B Value="65" />
			<Alpha Value="255" />
		</ControlOnDisabledForeground>
		<ControlOffDisabledForeground>
			<R Value="130" />
			<G Value="130" />
			<B Value="130" />
			<Alpha Value="255" />
		</ControlOffDisabledForeground>
		<ControlOnAlternativeForeground>
			<R Value="20" />
			<G Value="20" />
			<B Value="20" />
			<Alpha Value="255" />
		</ControlOnAlternativeForeground>
		<ControlTextBack>
			<R Value="62" />
			<G Value="62" />
			<B Value="62" />
			<Alpha Value="255" />
		</ControlTextBack>
		<ControlContrastFrame>
			<R Value="50" />
			<G Value="50" />
			<B Value="50" />
			<Alpha Value="255" />
		</ControlContrastFrame>
		<ControlSelectionFrame>
			<R Value="50" />
			<G Value="50" />
			<B Value="50" />
			<Alpha Value="255" />
		</ControlSelectionFrame>
		<ControlContrastTransport>
			<R Value="65" />
			<G Value="65" />
			<B Value="65" />
			<Alpha Value="255" />
		</ControlContrastTransport>
		<Progress>
			<R Value="32" />
			<G Value="183" />
			<B Value="255" />
			<Alpha Value="255" />
		</Progress>
		<ProgressText>
			<R Value="100" />
			<G Value="100" />
			<B Value="100" />
			<Alpha Value="255" />
		</ProgressText>
		<TransportProgress>
			<R Value="182" />
			<G Value="139" />
			<B Value="41" />
			<Alpha Value="255" />
		</TransportProgress>
		<ClipSlotButton>
			<R Value="65" />
			<G Value="65" />
			<B Value="65" />
			<Alpha Value="255" />
		</ClipSlotButton>
		<BrowserBar>
			<R Value="95" />
			<G Value="95" />
			<B Value="95" />
			<Alpha Value="255" />
		</BrowserBar>
		<BrowserBarOverlayHintTextColor>
			<R Value="160" />
			<G Value="160" />
			<B Value="160" />
			<Alpha Value="255" />
		</BrowserBarOverlayHintTextColor>
		<BrowserDisabledItem>
			<R Value="160" />
			<G Value="160" />
			<B Value="160" />
			<Alpha Value="255" />
		</BrowserDisabledItem>
		<BrowserSampleWaveform>
			<R Value="160" />
			<G Value="160" />
			<B Value="160" />
			<Alpha Value="255" />
		</BrowserSampleWaveform>
		<AutomationDisabled>
			<R Value="200" />
			<G Value="200" />
			<B Value="200" />
			<Alpha Value="255" />
		</AutomationDisabled>
		<AutomationMouseOver>
			<R Value="74" />
			<G Value="161" />
			<B Value="255" />
			<Alpha Value="255" />
		</AutomationMouseOver>
		<MidiNoteMaxVelocity>
			<R Value="255" />
			<G Value="88" />
			<B Value="76" />
			<Alpha Value="255" />
		</MidiNoteMaxVelocity>
		<RetroDisplayBackground>
			<R Value="40" />
			<G Value="40" />
			<B Value="40" />
			<Alpha Value="255" />
		</RetroDisplayBackground>
		<RetroDisplayBackgroundLine>
			<R Value="75" />
			<G Value="75" />
			<B Value="75" />
			<Alpha Value="255" />
		</RetroDisplayBackgroundLine>
		<RetroDisplayForeground>
			<R Value="0" />
			<G Value="182" />
			<B Value="242" />
			<Alpha Value="255" />
		</RetroDisplayForeground>
		<RetroDisplayForeground2>
			<R Value="109" />
			<G Value="215" />
			<B Value="255" />
			<Alpha Value="255" />
		</RetroDisplayForeground2>
		<RetroDisplayForegroundDisabled>
			<R Value="150" />
			<G Value="150" />
			<B Value="150" />
			<Alpha Value="255" />
		</RetroDisplayForegroundDisabled>
		<RetroDisplayGreen>
			<R Value="39" />
			<G Value="209" />
			<B Value="116" />
			<Alpha Value="255" />
		</RetroDisplayGreen>
		<RetroDisplayRed>
			<R Value="109" />
			<G Value="215" />
			<B Value="255" />
			<Alpha Value="255" />
		</RetroDisplayRed>
		<RetroDisplayHandle1>
			<R Value="21" />
			<G Value="180" />
			<B Value="255" />
			<Alpha Value="255" />
		</RetroDisplayHandle1>
		<RetroDisplayHandle2>
			<R Value="237" />
			<G Value="165" />
			<B Value="159" />
			<Alpha Value="255" />
		</RetroDisplayHandle2>
		<RetroDisplayScaleText>
			<R Value="255" />
			<G Value="255" />
			<B Value="255" />
			<Alpha Value="102" />
		</RetroDisplayScaleText>
		<ThresholdLineColor>
			<R Value="109" />
			<G Value="215" />
			<B Value="255" />
			<Alpha Value="255" />
		</ThresholdLineColor>
		<GainReductionLineColor>
			<R Value="0" />
			<G Value="216" />
			<B Value="240" />
			<Alpha Value="255" />
		</GainReductionLineColor>
		<InputCurveColor>
			<R Value="255" />
			<G Value="255" />
			<B Value="255" />
			<Alpha Value="38" />
		</InputCurveColor>
		<InputCurveOutlineColor>
			<R Value="0" />
			<G Value="0" />
			<B Value="0" />
			<Alpha Value="0" />
		</InputCurveOutlineColor>
		<OutputCurveColor>
			<R Value="214" />
			<G Value="221" />
			<B Value="228" />
			<Alpha Value="38" />
		</OutputCurveColor>
		<OutputCurveOutlineColor>
			<R Value="237" />
			<G Value="240" />
			<B Value="244" />
			<Alpha Value="255" />
		</OutputCurveOutlineColor>
		<SpectrumDefaultColor>
			<R Value="85" />
			<G Value="85" />
			<B Value="85" />
			<Alpha Value="255" />
		</SpectrumDefaultColor>
		<SpectrumAlternativeColor>
			<R Value="74" />
			<G Value="161" />
			<B Value="255" />
			<Alpha Value="255" />
		</SpectrumAlternativeColor>
		<SpectrumGridLines>
			<R Value="159" />
			<G Value="159" />
			<B Value="159" />
			<Alpha Value="85" />
		</SpectrumGridLines>
		<Operator1>
			<R Value="231" />
			<G Value="96" />
			<B Value="88" />
			<Alpha Value="255" />
		</Operator1>
		<Operator2>
			<R Value="61" />
			<G Value="224" />
			<B Value="4" />
			<Alpha Value="255" />
		</Operator2>
		<Operator3>
			<R Value="30" />
			<G Value="255" />
			<B Value="171" />
			<Alpha Value="255" />
		</Operator3>
		<Operator4>
			<R Value="51" />
			<G Value="189" />
			<B Value="255" />
			<Alpha Value="255" />
		</Operator4>
		<DrumRackScroller1>
			<R Value="0" />
			<G Value="0" />
			<B Value="0" />
			<Alpha Value="55" />
		</DrumRackScroller1>
		<DrumRackScroller2>
			<R Value="0" />
			<G Value="0" />
			<B Value="0" />
			<Alpha Value="90" />
		</DrumRackScroller2>
		<FilledDrumRackPad>
			<R Value="143" />
			<G Value="143" />
			<B Value="143" />
			<Alpha Value="255" />
		</FilledDrumRackPad>
		<SurfaceAreaFocus>
			<R Value="50" />
			<G Value="50" />
			<B Value="50" />
			<Alpha Value="255" />
		</SurfaceAreaFocus>
		<FreezeColor>
			<R Value="67" />
			<G Value="145" />
			<B Value="230" />
			<Alpha Value="255" />
		</FreezeColor>
		<GridLabel>
			<R Value="0" />
			<G Value="0" />
			<B Value="0" />
			<Alpha Value="128" />
		</GridLabel>
		<GridLineBase>
			<R Value="0" />
			<G Value="0" />
			<B Value="0" />
			<Alpha Value="255" />
		</GridLineBase>
		<ArrangerGridTiles>
			<R Value="0" />
			<G Value="0" />
			<B Value="0" />
			<Alpha Value="12" />
		</ArrangerGridTiles>
		<DetailGridTiles>
			<R Value="0" />
			<G Value="0" />
			<B Value="0" />
			<Alpha Value="10" />
		</DetailGridTiles>
		<GridGuideline>
			<R Value="195" />
			<G Value="195" />
			<B Value="195" />
			<Alpha Value="255" />
		</GridGuideline>
		<OffGridGuideline>
			<R Value="255" />
			<G Value="255" />
			<B Value="255" />
			<Alpha Value="95" />
		</OffGridGuideline>
		<TreeColumnHeadBackground>
			<R Value="120" />
			<G Value="120" />
			<B Value="120" />
			<Alpha Value="255" />
		</TreeColumnHeadBackground>
		<TreeColumnHeadForeground>
			<R Value="238" />
			<G Value="238" />
			<B Value="238" />
			<Alpha Value="255" />
		</TreeColumnHeadForeground>
		<TreeColumnHeadSelected>
			<R Value="110" />
			<G Value="110" />
			<B Value="110" />
			<Alpha Value="255" />
		</TreeColumnHeadSelected>
		<TreeColumnHeadFocus>
			<R Value="120" />
			<G Value="120" />
			<B Value="120" />
			<Alpha Value="255" />
		</TreeColumnHeadFocus>
		<TreeColumnHeadControl>
			<R Value="65" />
			<G Value="65" />
			<B Value="65" />
			<Alpha Value="255" />
		</TreeColumnHeadControl>
		<TreeRowCategoryForeground>
			<R Value="160" />
			<G Value="160" />
			<B Value="160" />
			<Alpha Value="255" />
		</TreeRowCategoryForeground>
		<TreeRowCategoryBackground>
			<R Value="0" />
			<G Value="0" />
			<B Value="0" />
			<Alpha Value="0" />
		</TreeRowCategoryBackground>
		<SearchIndication>
			<R Value="116" />
			<G Value="230" />
			<B Value="254" />
			<Alpha Value="255" />
		</SearchIndication>
		<SearchIndicationStandby>
			<R Value="67" />
			<G Value="164" />
			<B Value="222" />
			<Alpha Value="255" />
		</SearchIndicationStandby>
		<KeyZoneBackground>
			<R Value="205" />
			<G Value="216" />
			<B Value="179" />
			<Alpha Value="255" />
		</KeyZoneBackground>
		<KeyZoneCrossfadeRamp>
			<R Value="134" />
			<G Value="168" />
			<B Value="55" />
			<Alpha Value="255" />
		</KeyZoneCrossfadeRamp>
		<VelocityZoneBackground>
			<R Value="218" />
			<G Value="180" />
			<B Value="180" />
			<Alpha Value="255" />
		</VelocityZoneBackground>
		<VelocityZoneCrossfadeRamp>
			<R Value="218" />
			<G Value="78" />
			<B Value="78" />
			<Alpha Value="255" />
		</VelocityZoneCrossfadeRamp>
		<SelectorZoneBackground>
			<R Value="180" />
			<G Value="204" />
			<B Value="218" />
			<Alpha Value="255" />
		</SelectorZoneBackground>
		<SelectorZoneCrossfadeRamp>
			<R Value="85" />
			<G Value="119" />
			<B Value="198" />
			<Alpha Value="255" />
		</SelectorZoneCrossfadeRamp>
		<ViewCheckControlEnabledOff>
			<R Value="255" />
			<G Value="255" />
			<B Value="255" />
			<Alpha Value="127" />
		</ViewCheckControlEnabledOff>
		<ViewCheckControlDisabledOn>
			<R Value="238" />
			<G Value="238" />
			<B Value="238" />
			<Alpha Value="255" />
		</ViewCheckControlDisabledOn>
		<ViewCheckControlDisabledOff>
			<R Value="255" />
			<G Value="255" />
			<B Value="255" />
			<Alpha Value="64" />
		</ViewCheckControlDisabledOff>
		<DefaultBlendFactor Value="0.8000000119" />
		<IconBlendFactor Value="0.6499999762" />
		<ClipBlendFactor Value="0.75" />
		<NoteBorderStandbyBlendFactor Value="0.5" />
		<RetroDisplayBlendFactor Value="0.8999999762" />
		<CheckControlNotCheckedBlendFactor Value="0.5" />
		<MixSurfaceAreaBlendFactor Value="0.349999994" />
		<TextFrameSegmentBlendFactor Value="0.6000000238" />
		<VelocityEditorForegroundSelectedBlendFactor Value="0.6000000238" />
		<NoteDisabledSelectedBlendFactor Value="0.5" />
		<BackgroundClip>
			<R Value="92" />
			<G Value="92" />
			<B Value="92" />
			<Alpha Value="255" />
		</BackgroundClip>
		<BackgroundClipFrame>
			<R Value="70" />
			<G Value="70" />
			<B Value="70" />
			<Alpha Value="255" />
		</BackgroundClipFrame>
		<WarperTimeBarRulerBackground>
			<R Value="95" />
			<G Value="95" />
			<B Value="95" />
			<Alpha Value="255" />
		</WarperTimeBarRulerBackground>
		<WarperTimeBarMarkerBackground>
			<R Value="80" />
			<G Value="80" />
			<B Value="80" />
			<Alpha Value="255" />
		</WarperTimeBarMarkerBackground>
		<MinVelocityNoteBlendFactor Value="0.200000003" />
		<StripedBackgroundShadeFactor Value="0.8999999762" />
		<AutomationLaneHeaderAlpha Value="60" />
		<AutomationLaneClipBodyAlpha Value="60" />
		<NonEditableAutomationAlpha Value="127" />
		<DisabledContextMenuIconAlpha Value="85" />
		<BipolarPotiTriangle>
			<R Value="40" />
			<G Value="40" />
			<B Value="40" />
			<Alpha Value="255" />
		</BipolarPotiTriangle>
		<Poti>
			<R Value="40" />
			<G Value="40" />
			<B Value="40" />
			<Alpha Value="255" />
		</Poti>
		<DeactivatedPoti>
			<R Value="75" />
			<G Value="75" />
			<B Value="75" />
			<Alpha Value="255" />
		</DeactivatedPoti>
		<PotiNeedle>
			<R Value="40" />
			<G Value="40" />
			<B Value="40" />
			<Alpha Value="255" />
		</PotiNeedle>
		<DeactivatedPotiNeedle>
			<R Value="75" />
			<G Value="75" />
			<B Value="75" />
			<Alpha Value="255" />
		</DeactivatedPotiNeedle>
		<TransportOffBackground>
			<R Value="65" />
			<G Value="65" />
			<B Value="65" />
			<Alpha Value="255" />
		</TransportOffBackground>
		<TransportOffDisabledForeground>
			<R Value="120" />
			<G Value="120" />
			<B Value="120" />
			<Alpha Value="255" />
		</TransportOffDisabledForeground>
		<TransportSelectionBackground>
			<R Value="95" />
			<G Value="95" />
			<B Value="95" />
			<Alpha Value="255" />
		</TransportSelectionBackground>
		<Modulation>
			<R Value="109" />
			<G Value="215" />
			<B Value="255" />
			<Alpha Value="255" />
		</Modulation>
		<ModulationDisabled>
			<R Value="200" />
			<G Value="200" />
			<B Value="200" />
			<Alpha Value="255" />
		</ModulationDisabled>
		<ModulationMouseOver>
			<R Value="1" />
			<G Value="160" />
			<B Value="194" />
			<Alpha Value="255" />
		</ModulationMouseOver>
		<AutomationTransformToolFrame>
			<R Value="0" />
			<G Value="0" />
			<B Value="0" />
			<Alpha Value="63" />
		</AutomationTransformToolFrame>
		<AutomationTransformToolFrameActive>
			<R Value="0" />
			<G Value="0" />
			<B Value="0" />
			<Alpha Value="255" />
		</AutomationTransformToolFrameActive>
		<AutomationTransformToolHandle>
			<R Value="0" />
			<G Value="0" />
			<B Value="0" />
			<Alpha Value="63" />
		</AutomationTransformToolHandle>
		<AutomationTransformToolHandleActive>
			<R Value="0" />
			<G Value="0" />
			<B Value="0" />
			<Alpha Value="255" />
		</AutomationTransformToolHandleActive>
	</SkinManager>
	"""

	converted = convert_xml(xml_string)

	# write conversion result to file
	with open('converted.xml', 'w') as file:
		file.write(converted)

	# Print success message
	print('Conversion successful!')


if __name__ == "__main__":
    main()
